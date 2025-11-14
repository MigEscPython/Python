# -*- coding: utf-8 -*-
"""
Traducción funcional a Python del código Visual FoxPro proporcionado.
Propósito: replicar validaciones y actualizaciones en la base de datos
para uso legítimo (migración / soporte).
"""

import os
import sys
import datetime
import traceback

try:
    import wmi
except Exception:
    raise RuntimeError("Requiere el paquete 'wmi'. Instálalo: pip install wmi")

try:
    import pyodbc
except Exception:
    raise RuntimeError("Requiere el paquete 'pyodbc'. Instálalo: pip install pyodbc")


# ---------------------------
# Configuración por defecto (ajusta según tu entorno)
# ---------------------------
TCWEBADDRESS = "http://www.starsoft.com.py"  # usado en VFP para check de internet (no usado aquí)
NOMBRE_DIRECTORIO = r"C:\STARSOFT\BKP"
SISNOM = "NombreDelSistema"  # reemplaza por value real si corresponde
SISEXE = "*.exe"  # ejemplo, adaptalo si necesitas replicar ADIR
# Valores originales del VFP — se mantienen como fallback si los quieres:
DEFAULT_SERVER_1 = r"190.128.218.238\sqlexpress,49226"
DEFAULT_SERVER_2 = r"10.10.13.53\sqlexpress,49226"
DEFAULT_UID = "keys"
DEFAULT_PWD = "Sogan2016"
DEFAULT_DATABASE = "SystemKeys"
DEFAULT_DRIVER = "{SQL Server}"  # o "{ODBC Driver 17 for SQL Server}"


# ---------------------------
# Utilidades WMI / sistema
# ---------------------------

def get_disk_serial(drive_letter='C:'):
    """Obtener VolumeSerialNumber de la unidad (equivalente a FileSystemObject.drives('c').serialnumber)."""
    try:
        c = wmi.WMI()
        # Win32_LogicalDisk tiene VolumeSerialNumber en algunas implementaciones,
        # alternativamente podemos usar Win32_Volume
        for vol in c.Win32_LogicalDisk(DeviceID=drive_letter):
            vs = getattr(vol, "VolumeSerialNumber", None)
            if vs:
                # devolver como número (podía ser negativo en VFP), pero conservamos string
                return str(vs)
        # fallback: intentar Win32_Volume
        for vol in c.Win32_Volume():
            if vol.DriveLetter and vol.DriveLetter.upper() == drive_letter.upper():
                return str(getattr(vol, "SerialNumber", "") or getattr(vol, "DeviceID", ""))
    except Exception as e:
        print("Error obteniendo serial de disco:", e)
    return ""


def get_processor_id():
    """Obtener ProcessorId de Win32_Processor (equivalente a PROCESADOR procedure)."""
    try:
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            pid = getattr(cpu, "ProcessorId", None)
            if pid:
                return str(pid).strip()
    except Exception as e:
        print("Error obteniendo ProcessorId:", e)
    return ""


def get_ip_addresses():
    """Obtiene IPs (direcip1, direcip2) tal como ver_ip VFP."""
    ips = []
    try:
        c = wmi.WMI()
        for nic in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            addrs = getattr(nic, "IPAddress", None)
            if addrs:
                for a in addrs:
                    if a and a not in ips:
                        ips.append(a)
    except Exception as e:
        print("Error obteniendo IPs:", e)
    # Rellenar con '' si no hay suficientes
    while len(ips) < 2:
        ips.append("")
    return ips[0], ips[1]


# ---------------------------
# Backup / CSV / archivos
# ---------------------------

def check_backup_directory(nombre_directorio=NOMBRE_DIRECTORIO):
    """
    Busca archivos *.dat en nombre_directorio y devuelve:
    (bkp_flag ('SI'/'NO'), fecha_archivo (datetime or None), cantidad_archivos)
    """
    if not os.path.isdir(nombre_directorio):
        return "NO", None, 0

    files = []
    for entry in os.scandir(nombre_directorio):
        if entry.is_file() and entry.name.lower().endswith(".dat"):
            files.append(entry)

    if not files:
        return "NO", None, 0

    # buscar la fecha más reciente (modificación)
    latest = max(files, key=lambda f: f.stat().st_mtime)
    fecha_archivo = datetime.datetime.fromtimestamp(latest.stat().st_mtime).date()
    return "SI", fecha_archivo, len(files)


# ---------------------------
# Lectura conexion.dsn (simple parse)
# ---------------------------

def parse_conexion_dsn(path='conexion.dsn'):
    """
    Lee un archivo conexion.dsn y extrae SERVER, UID, DATABASE, PWD, TRUSTED_CONNECTION
    Devuelve dict con claves (server, uid, database, pwd, trusted).
    Si no existe, devuelve None
    """
    if not os.path.isfile(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            txt = f.read()
        # buscar líneas con KEY=VALUE
        def find_val(key):
            idx = txt.upper().find(key.upper() + '=')
            if idx < 0:
                return ''
            sub = txt[idx + len(key) + 1:]
            # toma hasta CR/LF
            for sep in ('\r', '\n'):
                p = sub.find(sep)
                if p >= 0:
                    sub = sub[:p]
                    break
            return sub.strip()

        server = find_val('SERVER')
        uid = find_val('UID')
        database = find_val('DATABASE')
        pwd = find_val('PWD')
        trusted = find_val('TRUSTED_CONNECTION') or find_val('TRUSTED')
        return {
            'server': server,
            'uid': uid,
            'database': database,
            'pwd': pwd,
            'trusted': trusted
        }
    except Exception as e:
        print("Error leyendo conexion.dsn:", e)
        return None


# ---------------------------
# SQL Server: conexión y operaciones (pyodbc)
# ---------------------------

def build_connection_string(driver, server, database, uid=None, pwd=None, trusted=False):
    """
    Construye connection string para pyodbc.
    """
    parts = []
    parts.append(f"DRIVER={driver}")
    parts.append(f"SERVER={server}")
    parts.append(f"DATABASE={database}")
    if trusted:
        parts.append("Trusted_Connection=yes")
    else:
        parts.append(f"UID={uid}")
        parts.append(f"PWD={pwd}")
    return ';'.join(parts)


def connect_with_fallbacks(primary_server, secondary_server, driver=DEFAULT_DRIVER,
                           uid=DEFAULT_UID, pwd=DEFAULT_PWD, database=DEFAULT_DATABASE, trusted=False):
    """Intenta conectarse al servidor primario y si falla intenta secundario."""
    # Intento 1
    conn_str = build_connection_string(driver, primary_server, database, uid=uid, pwd=pwd, trusted=trusted)
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        return conn
    except Exception as e1:
        print(f"No se pudo conectar a {primary_server}: {e1}")
        # Intentar servidor secundario
        if secondary_server:
            conn_str2 = build_connection_string(driver, secondary_server, database, uid=uid, pwd=pwd, trusted=trusted)
            try:
                conn2 = pyodbc.connect(conn_str2, timeout=5)
                return conn2
            except Exception as e2:
                print(f"No se pudo conectar a {secondary_server}: {e2}")
                return None
        return None


def sync_access_records(conn, accruc, sis, licencia, act_date, equipo, code, instalador, bkp_flag, fecha_archivo):
    """
    Reproduce la lógica VFP de insertar/actualizar en ACCESO y ACCESONIVEL.
    - conn: pyodbc.Connection
    - accruc: RUC
    - sis: sistema
    - licencia: licencia
    - act_date: fecha de activación (date)
    - equipo: nombre equipo (SYS(0) en VFP)
    - code: serial code
    - instalador: operador/instalador
    - bkp_flag: 'SI' o 'NO'
    - fecha_archivo: date or None
    """
    cursor = conn.cursor()
    try:
        # 1) SELECT * FROM ACCESO WHERE accruc=? AND accSis=?
        sql_select_acceso = "SELECT accruc, accSis, accLic, accFec, AccUc, AccAutoAct FROM ACCESO WHERE accruc=? AND accSis=?"
        cursor.execute(sql_select_acceso, (accruc, sis))
        acceso_row = cursor.fetchone()

        if acceso_row is None:
            # INSERT INTO ACCESO
            sql_insert_acceso = ("INSERT INTO ACCESO (accruc,accSis,accLic,accFec,AccUc,AccAutoAct) "
                                 "VALUES (?, ?, ?, ?, ?, 0)")
            cursor.execute(sql_insert_acceso, (accruc, sis, licencia, act_date, act_date))
            # INSERT INTO ACCESONIVEL
            sql_insert_accesonivel = ("INSERT INTO ACCESONIVEL "
                                      "(accruc,accSis,AccUc,AccSerial,AccBlock,AccInst,AccBkp,AccBkpFec,AccFecAct,AccNomEqui,AccServidor,AccFecIns) "
                                      "VALUES (?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?)")
            cursor.execute(sql_insert_accesonivel,
                           (accruc, sis, act_date, code, instalador, bkp_flag, fecha_archivo, act_date, equipo, '', act_date))
            conn.commit()
            return "inserted_both"
        else:
            # existe ACCESO
            # buscar en ACCESONIVEL por serial
            sql_select_accesonivel = "SELECT * FROM ACCESONIVEL WHERE AccSerial = ? AND accruc = ? AND accsis = ?"
            cursor.execute(sql_select_accesonivel, (code, accruc, sis))
            row_nivel = cursor.fetchone()
            if row_nivel is None:
                # Insertar ACCESONIVEL
                sql_insert_accesonivel = ("INSERT INTO ACCESONIVEL "
                                          "(accruc,accsis,AccUc,AccSerial,AccBlock,AccInst,AccBkp,AccBkpFec,AccFecAct,AccNomEqui,AccServidor) "
                                          "VALUES (?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?)")
                cursor.execute(sql_insert_accesonivel,
                               (accruc, sis, act_date, code, instalador, bkp_flag, fecha_archivo, act_date, equipo, ''))
                conn.commit()
                return "inserted_accesonivel"
            else:
                # Actualizar ACCESO (AccUc)
                sql_update_acceso = "UPDATE ACCESO SET AccUc = ? WHERE accruc = ? AND accSis = ?"
                cursor.execute(sql_update_acceso, (act_date, accruc, sis))
                # Actualizar ACCESONIVEL según VFP
                sql_update_nivel = ("UPDATE ACCESONIVEL SET AccUc=?, AccInst=?, AccBkp=?, AccBkpFec=?, AccFecAct=?, AccNomEqui=?, AccServidor=? "
                                    "WHERE accruc = ? AND accsis = ? AND AccSerial = ?")
                cursor.execute(sql_update_nivel, (act_date, instalador, bkp_flag, fecha_archivo, act_date, equipo, '', accruc, sis, code))
                conn.commit()
                return "updated"
    except Exception as e:
        conn.rollback()
        print("Error en sync_access_records:", e)
        traceback.print_exc()
        raise
    finally:
        cursor.close()


# ---------------------------
# Flujo principal (equivalente a la rutina principal VFP)
# ---------------------------

def main(sistemnom=SISNOM, sisexe=SISEXE):
    # Variables equivalentes
    serieplaca = ""
    _code = ""
    _fechasis = None
    _procesador = ""
    _direcip1 = ""
    _direcip2 = ""
    servidor_flag = ''
    _bkp = 'NO'
    fecha_archivo = None
    nombre_directorio = NOMBRE_DIRECTORIO

    # obtenemos serial disco y procesador
    lcserialnumber = get_disk_serial('C:')
    # en VFP multiplicaba por -1 si negativo; aquí mantenemos string
    _procesador = get_processor_id()
    _code = (lcserialnumber or '') + '-' + (_procesador or '')

    # obtener lista archivos (simulación ADIR)
    # _act = fm(1,3) en VFP era versión del exe; aquí lo dejamos como fecha actual o se lee de alguna fuente
    _act = datetime.date.today().isoformat()
    _fecha = datetime.date.today()
    _sis = sistemnom
    _equipo = os.environ.get('COMPUTERNAME', '')

    # comprobar backup
    _bkp, fecha_archivo, c_directorio = check_backup_directory(nombre_directorio)

    # ver servidor / leer conexion.dsn
    ips = get_ip_addresses()
    _direcip1, _direcip2 = ips

    dsn_config = parse_conexion_dsn('conexion.dsn')
    _server = None
    _uid = None
    _database = None
    _pwd = None
    _trusted = False
    if dsn_config:
        _server = dsn_config.get('server') or None
        _uid = dsn_config.get('uid') or None
        _database = dsn_config.get('database') or None
        _pwd = dsn_config.get('pwd') or None
        _trusted = (dsn_config.get('trusted', '').upper() in ('YES', 'TRUE', '1'))
        # determinar nombre servidor (antes de la '\')
        if _server:
            nombre_serv = _server.split('\\')[0]
        else:
            nombre_serv = ''
    else:
        nombre_serv = ''

    # determinar si este equipo es servidor (lógica de ver_srv)
    _nombre_equipo = _equipo
    version_win = None  # en VFP se usó OS(1)
    if nombre_serv:
        if nombre_serv.strip().upper() == _nombre_equipo.strip().upper() or nombre_serv.strip().upper() == '(LOCAL)':
            servidor_flag = 'SI'
        elif nombre_serv.strip() == _direcip1 or nombre_serv.strip() == _direcip2:
            servidor_flag = 'SI'
        else:
            servidor_flag = 'NO'
    else:
        servidor_flag = ''

    # leer datos locales (simulación: en VFP abría C:\STARSOFT\Milegold para obtener operador y fecha)
    # aquí asumimos que tienes esos valores disponibles o pides al usuario:
    instalador = os.environ.get('USERNAME', 'instalador')
    fecha_lic = datetime.date.today()

    # Datos de conexión por defecto (como en VFP)
    # Primero intentamos usar conexión especificada en conexion.dsn; si no existe, usar valores por defecto del código VFP
    conn_server = _server if _server else DEFAULT_SERVER_1
    conn_uid = _uid if _uid else DEFAULT_UID
    conn_pwd = _pwd if _pwd else DEFAULT_PWD
    conn_database = _database if _database else DEFAULT_DATABASE
    conn_trusted = _trusted

    # Intentar conectar con fallback (similar a SQLSTRINGCONNECT y reintentos)
    conn = connect_with_fallbacks(conn_server, DEFAULT_SERVER_2, driver=DEFAULT_DRIVER,
                                  uid=conn_uid, pwd=conn_pwd, database=conn_database, trusted=conn_trusted)
    if not conn:
        print("NO PUDO CONECTARSE a ningún servidor SQL configurado. Abortando.")
        return

    try:
        # Ejecutar la sincronización equivalente a las instrucciones VFP de INSERT/UPDATE en ACCESO y ACCESONIVEL
        resultado = sync_access_records(conn,
                                        accruc='',  # en VFP venía de hab.ruc; aquí debes pasar RUC válido
                                        sis=_sis,
                                        licencia='',  # hab.licencia
                                        act_date=datetime.date.today(),
                                        equipo=_equipo,
                                        code=_code,
                                        instalador=instalador,
                                        bkp_flag=_bkp,
                                        fecha_archivo=fecha_archivo)
        print("Resultado de sincronización:", resultado)
    finally:
        conn.close()


if __name__ == "__main__":
    # Ejecuta el flujo principal.
    # Nota: Rellena las variables de RUC y licencia antes de usar en entorno productivo.
    main()
