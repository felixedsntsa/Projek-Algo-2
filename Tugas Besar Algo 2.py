import os
import csv
import sys
import pandas as pd
import colorama 
import getpass
from pathlib import Path
from tabulate import tabulate
from colorama import Back,Fore, Style

session = '' 

#Warna
colorama.init(autoreset=True)
ungu_gelap = Fore.MAGENTA + Style.DIM
ungu_terang = Fore.MAGENTA + Style.BRIGHT
putih_terang = Fore.WHITE + Style.BRIGHT
putih_gelap = Fore.WHITE + Style.DIM

def Dashboard()->None:
    os.system("cls")

    print(ungu_gelap+"="*80)
    print(putih_terang+"SELAMAT DATANG".center(80))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(80))
    print(ungu_gelap+ "="*80)

def tambahData(): 
    os.system('cls') 

    merk = input("Masukkan merk unit: ")
    tipe = input("Masukkan tipe unit: ")
    kelengkapan = input("Masukkan kelengkapan unit: ")
    harga = int(input("Masukkan harga sewa unit/hari: "))    

    entry = {'merk': merk, 'tipe': tipe, 'kelengkapan': kelengkapan, 'harga': harga}
    tambah_id('unit.csv', entry)
    
    os.system('cls') 
    print("Data berhasil ditambahkan!\n")
    input("\nEnter untuk lanjutkan")
    os.system('cls') 
    unit()

def getData():
    df = pd.read_csv('unit.csv')
    df.reset_index(drop=True, inplace=True)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    return df

def lihatData():
    os.system('cls')

    getData()

    while True: 
    
        print('''
Pilihan :
    [1] Cari Data Unit
    [2] Urutkan Data Unit
              
    [0] Kembali ke Menu Unit
              ''')
    
        menu = input("Masukkan pilihan anda = ")

        if menu == "1":
            cariData() 
        elif menu == "2":
            os.system('cls')
            order = input("[1. Harga Sewa Termurah][2. Harga Sewa Termahal]: ")
            urutkanData(order)
        elif menu == "0":
            unit() 
        else:
            os.system('cls')
            input("\n Pilihan tidak sesuai, enter untuk kembali") 
        lihatData()

def editData():
    os.system('cls')

    getData()
    
    df = pd.read_csv('unit.csv')

    try:
        edit = int(input("Pilih ID yang ingin diedit: "))
        if edit in df['id'].values:
            merkBaru = input("Masukkan merk unit baru: ")
            tipeBaru = input("Masukkan tipe unit baru: ")
            kelengkapanBaru = input("Masukkan kelengkapan unit baru: ")
            hargaBaru = int(input("Masukkan harga sewa unit/hari baru: ")) 

            index_to_edit = df[df['id'] == edit].index[0]
            df.at[index_to_edit, 'merk'] = merkBaru
            df.at[index_to_edit, 'tipe'] = tipeBaru
            df.at[index_to_edit, 'kelengkapan'] = kelengkapanBaru
            df.at[index_to_edit, 'harga'] = hargaBaru

            df.to_csv('unit.csv', index=False)
            print("Data berhasil diedit")
        else:
            print("ID tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.")

    input("\nEnter untuk lanjut")
    unit()

def hapusData():
    os.system('cls')

    getData()
    
    df = pd.read_csv('unit.csv')

    try:
        row_to_delete = int(input("Masukkan ID yang ingin dihapus: ")) 
        if row_to_delete in df['id'].values: 
            df = df[df['id'] != row_to_delete].reset_index(drop=True) 
            df.to_csv('unit.csv', index=False) 
            print("Data berhasil dihapus.")
        else:
            print("ID tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.") 

    input("\nEnter untuk lanjut.")
    unit()    

def binary_search(df, merk, tipe):
    left, right = 0, len(df) - 1
    merk = merk.lower()
    tipe = tipe.lower()

    while left <= right:
        mid = (left + right) // 2
        mid_value_merk = df.at[mid, 'merk'].lower()
        mid_value_tipe = df.at[mid, 'tipe'].lower()
        
        if mid_value_merk == merk and mid_value_tipe == tipe:
            return mid
        elif mid_value_merk < merk or (mid_value_merk == merk and mid_value_tipe < tipe):
            left = mid + 1
        else:
            right = mid - 1
    return -1

def cariData():
    os.system('cls')

    df = pd.read_csv('unit.csv')
    df = df.sort_values(['merk', 'tipe']).reset_index(drop=True) 

    merk = input("Masukkan merk unit yang ingin dicari: ")
    tipe = input("Masukkan tipe unit yang ingin dicari: ")
    
    index = binary_search(df, merk, tipe)

    if index != -1:
        print("Data ditemukan:")
        print(tabulate(df.iloc[[index]], headers='keys', tablefmt='grid', showindex=False))
    else:
        os.system('cls')
        print("Data dengan merk dan tipe tersebut tidak ditemukan.")

    input("\nEnter untuk lanjut")
    lihatData()

def quick_sort(arr, low, high, key):
    if low < high:
        pi = partisi(arr, low, high, key)
        quick_sort(arr, low, pi - 1, key)
        quick_sort(arr, pi + 1, high, key)

def partisi(arr, low, high, key):
    pivot = arr[high][key]
    i = low - 1
    for j in range(low, high):
        if arr[j][key] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def urutkanData(order='asc'):
    os.system('cls')

    df = pd.read_csv('unit.csv')
    data = df.to_dict(orient='records')

    if order == "1":
        quick_sort(data, 0, len(data) - 1, 'harga')
    else:
        quick_sort(data, 0, len(data) - 1, 'harga')
        data = data[::-1]

    sorted_df = pd.DataFrame(data)
    print(tabulate(sorted_df, headers='keys', tablefmt='grid', showindex=False))

    input("\nEnter untuk lanjut")
    lihatData()

def create_csv(file_path, header):
    if not Path(file_path).is_file(): 
        with open(file_path, 'w', newline='') as filecsv: 
            csv_writer = csv.DictWriter(filecsv, fieldnames=['id'] + header, delimiter=',')
            csv_writer.writeheader()

def tambah_id(file_path, entry):
    if Path(file_path).is_file():
        with open(file_path, 'r+', newline='') as filecsv:
            csv_reader = csv.DictReader(filecsv)
            existing_entries = list(csv_reader)
            next_id = len(existing_entries) + 1
            entry_with_id = {'id': next_id}
            entry_with_id.update(entry)
            
            filecsv.seek(0, os.SEEK_END)  
            csv_writer = csv.DictWriter(filecsv, fieldnames=csv_reader.fieldnames)
            csv_writer.writerow(entry_with_id)

def awal():
    os.system('cls')

    create_csv('unit.csv', ['merk', 'tipe', 'kelengkapan', 'harga'])
    create_csv('admin.csv', ['username', 'email', 'no_telepon', 'password'])
    create_csv('customer.csv', ['nama', 'nik', 'no_telepon'])
    create_csv('transaksi.csv', ['customer', 'tanggal_peminjaman', 'tanggal_pengembalian', 'unit', 'admin', 'metode_pembayaran', 'status_pembayaran'])

    Dashboard()
    
    print('''
Pilihan :
    [1] Registrasi
    [2] Login
              
    [0] Keluar
            ''')
    
    user_type = input("Masukkan pilihan anda = ")

    if user_type == "1":
        daftar_admin()
    elif user_type == "2":
        masuk_admin()
    elif user_type == "0":
        keluar()
    else:
        os.system('cls')
        input("Masukkan pilihan yang ada\nUntuk melanjutkan, tekan enter") 
        awal()

def keluar():
    os.system('cls')

    print(ungu_gelap+"="*80)
    print(putih_terang+"TERIMAKASIH TELAH MENGGUNAKAN".center(80))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(80))
    print(ungu_gelap+ "="*80)
    sys.exit()

def admin_menu():
    os.system("cls")

    print(ungu_gelap+"="*80)
    print(putih_terang+"ADMIN MENU".center(80))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(80))
    print(ungu_gelap+ "="*80)

    while True: 
    
        print('''
Pilihan :
    [1] Unit
    [2] Customer
    [3] Transaksi
              
    [0] Kembali ke Halaman Awal
              ''')
    
        menu = input("Masukkan pilihan anda = ")

        if menu == "1":
            unit() 
        elif menu == "2":
            customer() 
        elif menu == "3":
            transaksi()
        elif menu == "0":
            awal() 
        else:
            os.system('cls')
            input("\n Pilihan tidak sesuai, enter untuk kembali ke menu admin") 
        admin_menu()

def validasi_admin(email, password):
    with open("admin.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["email"] == email and row["password"] == password:
                return True
    return False 

def cek_user_admin(username):
    with open("admin.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["username"] == username:
                print("Akun Sudah Tersedia. Silahkan coba lagi") 
                input("Untuk melanjutkan, tekan enter")
                awal()
                return True
    return False

def daftar_admin():
    os.system('cls')

    Dashboard()

    username = input("Masukkan nama: ") 

    if cek_user_admin(username):
        print("Username sudah ada, silahkan coba lagi")
        return

    email = input("Masukkan Email: ")
    no_telepon = input("Masukkan No Telepon: ")
    password = input("Masukkan Password: ")

    entry = {
        'username': username,
        'email': email,
        'no_telepon': no_telepon,
        'password': password
    }

    tambah_id('admin.csv', entry)

    input("Data telah ditambahkan\nUntuk melanjutkan, tekan enter") 
    awal() 

def masuk_admin():
    os.system('cls')

    Dashboard()

    while True:

        global session

        email = input("Masukkan email: ") 
        password = getpass.getpass("Masukkan password: ") 

        if validasi_admin(email, password):

            session = email
            os.system("cls")
            admin_menu()
            break
        else:
            input("Masukkan data yang benar!\nTekan enter untuk melanjutkan.") 
        awal()

def unit():
    os.system("cls")

    print(ungu_gelap+"="*80)
    print(putih_terang+"UNIT MENU".center(80))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(80))
    print(ungu_gelap+ "="*80)

    while True:

        print('''
Pilihan :
    [1] Tambah Data Unit
    [2] Lihat Data Unit
    [3] Edit Data Unit
    [4] Hapus Data Unit
              
    [0] Kembali ke Menu Utama
              ''')
        
        menu = input("Masukkan pilihan anda = ")

        if menu == "1":
            tambahData() 
        elif menu == "2":
            lihatData() 
        elif menu == "3":
            editData() 
        elif menu == "4":
            hapusData()
        elif menu == "0":
            admin_menu() 
        else:
            os.system('cls')
            input("\n Pilihan tidak sesuai, enter untuk kembali ke menu unit") 
        unit()

def tambahCustomer(): 
    os.system('cls') 

    nama = input("Masukkan nama: ")
    nik = input("Masukkan nik: ")
    telepon = input("Masukkan no telepon: ")   

    entry = {'nama': nama, 'nik': nik, 'no_telepon': telepon}
    tambah_id('customer.csv', entry)
    
    os.system('cls') 
    print("Data berhasil ditambahkan!\n")
    input("\nEnter untuk lanjutkan")
    os.system('cls') 
    customer()

def lihatCustomer():
    os.system('cls')

    getCustomer()

    while True: 
    
        print('''
Pilihan :
    [1] Cari Data Customer
              
    [0] Kembali ke Menu Customer
              ''')
    
        menu = input("Masukkan pilihan anda = ")

        if menu == "1":
            cariCustomer() 
        elif menu == "0":
            customer() 
        else:
            os.system('cls')
            input("\n Pilihan tidak sesuai, enter untuk kembali") 
        lihatCustomer()

def getCustomer():
    df = pd.read_csv('customer.csv', dtype={'nik': str, 'no_telepon': str})
    df.reset_index(drop=True, inplace=True)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    return df

def editCustomer():
    os.system('cls')

    df = getCustomer()

    try:
        edit = int(input("Pilih ID yang ingin diedit: "))
        if edit in df['id'].values:
            namaBaru = input("Masukkan nama baru: ")
            nikBaru = input("Masukkan nik baru: ")
            teleponBaru = input("Masukkan no_telepon baru: ")

            df['nik'] = df['nik'].astype(str)
            df['no_telepon'] = df['no_telepon'].astype(str)

            index_to_edit = df[df['id'] == edit].index[0]
            df.at[index_to_edit, 'nama'] = namaBaru
            df.at[index_to_edit, 'nik'] = nikBaru
            df.at[index_to_edit, 'no_telepon'] = teleponBaru

            df.to_csv('customer.csv', index=False)
            print("Data berhasil diedit")
        else:
            print("ID tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.")

    input("\nEnter untuk lanjut")
    customer()

def hapusCustomer():
    os.system('cls')

    getCustomer()
    
    df = pd.read_csv('customer.csv')

    try:
        row_to_delete = int(input("Masukkan ID yang ingin dihapus: ")) 
        if row_to_delete in df['id'].values: 
            df = df[df['id'] != row_to_delete].reset_index(drop=True) 
            df.to_csv('customer.csv', index=False) 
            print("Data berhasil dihapus.")
        else:
            print("ID tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.") 

    input("\nEnter untuk lanjut.")
    customer()    

def binary_search_cust(df, nama):
    left, right = 0, len(df) - 1
    nama = nama.lower()

    while left <= right:
        mid = (left + right) // 2
        mid_value_nama = df.at[mid, 'nama'].lower()
        
        if mid_value_nama == nama:
            return mid
        elif mid_value_nama < nama: 
            left = mid + 1
        else:
            right = mid - 1
    return -1

def cariCustomer():
    os.system('cls')

    df = pd.read_csv('customer.csv')
    df = df.sort_values(['nama']).reset_index(drop=True)  

    nama = input("Masukkan nama yang ingin dicari: ")
    
    index = binary_search_cust(df, nama)

    if index != -1:
        print("Data ditemukan:")
        print(tabulate(df.iloc[[index]], headers='keys', tablefmt='grid', showindex=False))
    else:
        os.system('cls')
        print("Data dengan merk dan tipe tersebut tidak ditemukan.")

    input("\nEnter untuk lanjut")
    lihatCustomer()

def customer():
    os.system("cls")

    print(ungu_gelap+"="*80)
    print(putih_terang+"CUSTOMER MENU".center(80))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(80))
    print(ungu_gelap+ "="*80)

    while True:

        print('''
Pilihan :
    [1] Tambah Data Customer
    [2] Lihat Data Customer
    [3] Edit Data Customer
    [4] Hapus Data Customer
              
    [0] Kembali ke Menu Utama
              ''')
        
        menu = input("Masukkan pilihan anda = ")

        if menu == "1":
            tambahCustomer() 
        elif menu == "2":
            lihatCustomer() 
        elif menu == "3":
            editCustomer() 
        elif menu == "4":
            hapusCustomer()
        elif menu == "0":
            admin_menu() 
        else:
            os.system('cls')
            input("\n Pilihan tidak sesuai, enter untuk kembali ke menu unit") 
        customer()

def tambahTransaksi(): 
    os.system('cls')
    
    global session

    print("Daftar Customer:")
    customer_df = getCustomer()
    customer_id = input("Pilih ID customer: ")
    
    if customer_id.isdigit() and int(customer_id) in customer_df['id'].values:
        customer_name = customer_df.loc[customer_df['id'] == int(customer_id), 'nama'].values[0]
    else:
        print("ID customer tidak valid!")
        return

    print("\nDaftar Unit:")
    unit_df = getData()
    unit_id = input("Pilih ID unit: ")

    if unit_id.isdigit() and int(unit_id) in unit_df['id'].values:
        unit_merk = unit_df.loc[unit_df['id'] == int(unit_id), 'merk'].values[0]
        unit_tipe = unit_df.loc[unit_df['id'] == int(unit_id), 'tipe'].values[0]
        unit_name = f"{unit_merk} {unit_tipe}"
    else:
        print("ID unit tidak valid!")
        return

    tanggal_peminjaman = input("Masukkan tanggal peminjaman: ")
    tanggal_pengembalian = input("Masukkan tanggal pengembalian: ")
    admin = session
    metode_pembayaran = input("Masukkan metode pembayaran: ")  
    status_pembayaran = input("Masukkan status pembayaran: ")  

    entry = {
        'customer': customer_name, 
        'tanggal_peminjaman': tanggal_peminjaman, 
        'tanggal_pengembalian': tanggal_pengembalian,
        'unit': unit_name,
        'admin': admin,
        'metode_pembayaran': metode_pembayaran,
        'status_pembayaran': status_pembayaran
    }
    
    tambah_id('transaksi.csv', entry)
    
    os.system('cls') 
    print("Data berhasil ditambahkan!\n")
    input("\nEnter untuk lanjutkan")
    os.system('cls') 
    transaksi()

def getTransaksi():
    df = pd.read_csv('transaksi.csv')
    df.reset_index(drop=True, inplace=True)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    return df

def hapusTransaksi():
    os.system('cls')

    getTransaksi()
    
    df = pd.read_csv('transaksi.csv')

    try:
        row_to_delete = int(input("Masukkan ID yang ingin dihapus: ")) 
        if row_to_delete in df['id'].values: 
            df = df[df['id'] != row_to_delete].reset_index(drop=True) 
            df.to_csv('transaksi.csv', index=False) 
            print("Data berhasil dihapus.")
        else:
            print("ID tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.") 

    input("\nEnter untuk lanjut.")
    transaksi()   

def riwayat():
    os.system('cls')

    getTransaksi()

    while True: 
    
        print('''
Pilihan :
    [1] Cari Data Transaksi
    [2] Urutkan Data Transaksi
              
    [0] Kembali ke Menu Transaksi
              ''')
    
        menu = input("Masukkan pilihan anda = ")

        if menu == "1":
            cariTransaksi()
        elif menu == "2":
            os.system('cls')
            order = input("[1. Transkasi Terbaru][2. Transaksi Terlama]: ")
            urutkanTransaksi(order) 
        elif menu == "0":
            transaksi() 
        else:
            os.system('cls')
            input("\n Pilihan tidak sesuai, enter untuk kembali") 
        riwayat()

def cariTransaksi():
    os.system('cls')

    df = pd.read_csv('transaksi.csv')

    print('''
Cari berdasarkan:
    [1] Tanggal Peminjaman
    [2] Tanggal Pengembalian
    ''')
    pilihan = input("Masukkan pilihan anda: ")
    
    if pilihan == '1':
        date_column = 'tanggal_peminjaman'
    elif pilihan == '2':
        date_column = 'tanggal_pengembalian'
    else:
        os.system('cls')
        print("Pilihan tidak sesuai, enter untuk kembali")
        input()
        return
    
    date = input(f"Masukkan {date_column.replace('_', ' ')} yang ingin dicari (dd-mm-yyyy): ")

    hasil = linear_search_trans(df, date, date_column)

    if not hasil.empty:
        os.system('cls')
        print("Data ditemukan:")
        print(tabulate(hasil, headers='keys', tablefmt='grid', showindex=False))
    else:
        os.system('cls')
        print(f"Data dengan {date_column.replace('_', ' ')} tersebut tidak ditemukan.")

    input("\nEnter untuk lanjut")
    riwayat()

def linear_search_trans(df, date, date_column):
    return df[df[date_column] == date]

def quick_sort_trans(arr, low, high, key):
    if low < high:
        pi = partisi_trans(arr, low, high, key)
        quick_sort_trans(arr, low, pi - 1, key)
        quick_sort_trans(arr, pi + 1, high, key)

def partisi_trans(arr, low, high, key):
    pivot = date_to_tuple(arr[high][key])
    i = low - 1
    for j in range(low, high):
        if date_to_tuple(arr[j][key]) < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def date_to_tuple(date_str):
    day, month, year = map(int, date_str.split('-'))
    return (year, month, day)

def urutkanTransaksi(order='1'):
    os.system('cls')

    df = pd.read_csv('transaksi.csv')
    data = df.to_dict(orient='records')

    if order == "1":
        quick_sort_trans(data, 0, len(data) - 1, 'tanggal_peminjaman')
        data = data[::-1]
    else:
        quick_sort_trans(data, 0, len(data) - 1, 'tanggal_peminjaman')

    sorted_df = pd.DataFrame(data)
    print(tabulate(sorted_df, headers='keys', tablefmt='grid', showindex=False))

    input("\nEnter untuk lanjut")
    riwayat()

def transaksi():
    os.system("cls")

    print(ungu_gelap+"="*80)
    print(putih_terang+"TRANSACTION MENU".center(80))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(80))
    print(ungu_gelap+ "="*80)

    while True:

        print('''
Pilihan :
    [1] Tambah Data Transaksi
    [2] Hapus Data Transaksi
    [3] Riwayat Transaksi
              
    [0] Kembali ke Menu Utama
              ''')
        
        menu = input("Masukkan pilihan anda = ")

        if menu == "1":
            tambahTransaksi()
        elif menu == "2":
            hapusTransaksi() 
        elif menu == "3":
            riwayat() 
        elif menu == "0":
            admin_menu() 
        else:
            os.system('cls')
            input("\n Pilihan tidak sesuai, enter untuk kembali ke menu unit") 
        transaksi()

if __name__ == "__main__":
    awal()
