import argparse
import subprocess

def migrate_server(src_server, src_user, src_password, dest_server, dest_user, dest_password):
    print(f"Migrating all databases from server {src_server} to server {dest_server}")

    # Dump all databases from source server
    dump_cmd = [
        "mysqldump",
        "-h", src_server,
        "-u", src_user,
        f"-p{src_password}",
        "--all-databases"
    ]
    with open("all_databases.sql", "w") as dump_file:
        subprocess.run(dump_cmd, stdout=dump_file)
    
    # Import the dump into destination server
    import_cmd = [
        "mysql",
        "-h", dest_server,
        "-u", dest_user,
        f"-p{dest_password}"
    ]
    with open("all_databases.sql", "r") as dump_file:
        subprocess.run(import_cmd, stdin=dump_file)
    
    print("Migration completed successfully.")

def migrate_db(src_server, src_user, src_password, src_db, dest_server, dest_user, dest_password, dest_db=None):
    if not dest_db:
        dest_db = src_db

    print(f"Migrating database {src_db} from server {src_server} to {dest_db} on server {dest_server}")

    # Dump the specific database from source server
    dump_cmd = [
        "mysqldump",
        "-h", src_server,
        "-u", src_user,
        f"-p{src_password}",
        src_db
    ]
    dump_file_name = f"{src_db}.sql"
    with open(dump_file_name, "w") as dump_file:
        subprocess.run(dump_cmd, stdout=dump_file)
    
    # Import the dump into the destination server
    import_cmd = [
        "mysql",
        "-h", dest_server,
        "-u", dest_user,
        f"-p{dest_password}",
        dest_db
    ]
    with open(dump_file_name, "r") as dump_file:
        subprocess.run(import_cmd, stdin=dump_file)
    
    print("Database migration completed successfully.")

def migrate_table(src_server, src_user, src_password, src_db, src_table, dest_server, dest_user, dest_password, dest_db=None, dest_table=None):
    if not dest_db:
        dest_db = src_db
    if not dest_table:
        dest_table = src_table

    print(f"Migrating table {src_table} from {src_db} on server {src_server} to {dest_table} in {dest_db} on server {dest_server}")

    # Dump the specific table from source server
    dump_cmd = [
        "mysqldump",
        "-h", src_server,
        "-u", src_user,
        f"-p{src_password}",
        src_db,
        src_table
    ]
    dump_file_name = f"{src_table}.sql"
    with open(dump_file_name, "w") as dump_file:
        subprocess.run(dump_cmd, stdout=dump_file)
    
    # Import the dump into the destination server
    import_cmd = [
        "mysql",
        "-h", dest_server,
        "-u", dest_user,
        f"-p{dest_password}",
        dest_db
    ]
    with open(dump_file_name, "r") as dump_file:
        subprocess.run(import_cmd, stdin=dump_file)
    
    print("Table migration completed successfully.")

def main():
    parser = argparse.ArgumentParser(description='DB migration tool')
    
    subparsers = parser.add_subparsers(dest='mode', required=True, help='Migration mode: server / db / table')

    server_parser = subparsers.add_parser('server', help='Server migration')
    server_parser.add_argument('src_server', help='Source server')
    server_parser.add_argument('src_user', help='Source server user')
    server_parser.add_argument('src_password', help='Source server password')
    server_parser.add_argument('dest_server', help='Destination server')
    server_parser.add_argument('dest_user', help='Destination server user')
    server_parser.add_argument('dest_password', help='Destination server password')

    db_parser = subparsers.add_parser('db', help='Database migration')
    db_parser.add_argument('src_server', help='Source server')
    db_parser.add_argument('src_user', help='Source server user')
    db_parser.add_argument('src_password', help='Source server password')
    db_parser.add_argument('src_db', help='Source database')
    db_parser.add_argument('dest_server', help='Destination server')
    db_parser.add_argument('dest_user', help='Destination server user')
    db_parser.add_argument('dest_password', help='Destination server password')
    db_parser.add_argument('dest_db', nargs='?', help='Destination database (default: same as source database)')

    table_parser = subparsers.add_parser('table', help='Table migration')
    table_parser.add_argument('src_server', help='Source server')
    table_parser.add_argument('src_user', help='Source server user')
    table_parser.add_argument('src_password', help='Source server password')
    table_parser.add_argument('src_db', help='Source database')
    table_parser.add_argument('src_table', help='Source table')
    table_parser.add_argument('dest_server', help='Destination server')
    table_parser.add_argument('dest_user', help='Destination server user')
    table_parser.add_argument('dest_password', help='Destination server password')
    table_parser.add_argument('dest_db', nargs='?', help='Destination database (default: same as source database)')
    table_parser.add_argument('dest_table', nargs='?', help='Destination table (default: same as source table)')

    args = parser.parse_args()

    if args.mode == 'server':
        migrate_server(args.src_server, args.src_user, args.src_password, args.dest_server, args.dest_user, args.dest_password)
    elif args.mode == 'db':
        migrate_db(args.src_server, args.src_user, args.src_password, args.src_db, args.dest_server, args.dest_user, args.dest_password, args.dest_db)
    elif args.mode == 'table':
        migrate_table(args.src_server, args.src_user, args.src_password, args.src_db, args.src_table, args.dest_server, args.dest_user, args.dest_password, args.dest_db, args.dest_table)

if __name__ == '__main__':
    main()
