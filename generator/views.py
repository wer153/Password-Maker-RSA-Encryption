from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.
def home(request):
    return render(request, 'generator/home.html', {'password':'mypassword'})

def creator(request):
    return render(request, 'generator/creator.html')

def password(request):
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    special = '!@#$%^&*()_+|'
    numbers = '0123456789'

    characters = list(alphabet)

    if request.GET.get('uppercase'):
        characters.extend(alphabet.upper())
    if request.GET.get('special'):
        characters.extend(special)
    if request.GET.get('numbers'):
        characters.extend(numbers)

    length = int(request.GET.get('length'),12)

    thepassword = ''.join([ random.choice(characters) for x in range(length)])

    return render(request, 'generator/password.html', {'password':thepassword})

def encrypt(request):
    
    def gcd(a, b):
        while b!=0:
            a, b = b, a%b
        return a

    def get_public_key(totient):
        e=2
        while(e<totient and gcd(e, totient)!=1):
            e+=1
        return e

    def get_private_key(public_key, totient):
        k=1
        while (public_key*k)%totient != 1 or k == public_key:
            k+=1
        return k

    def get_encrypt_message(pk, plain_text):
        key, n = pk
        return '#'.join([str((ord(char)**key) % n) for char in plain_text])

    prime_numbers = [601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597 ]
    p, q = random.sample(prime_numbers, 2)
    n = p*q
    totient = (p-1)*(q-1)

    passwords = {}
    passwords['original_password'] = request.GET.get('original_password')

    public_key = get_public_key(totient) #e
    private_key = get_private_key(public_key, totient) #d

    passwords['key_pair'] = (private_key,n)
    passwords['encrypted_message'] = get_encrypt_message((public_key,n), passwords['original_password'])
    
    return render(request, 'generator/encrypt.html', passwords)

def decrypt(request):
    
    def get_original_password(cipher, key_pair):
        key, n = map(int,key_pair.split(','))
        return ''.join([chr((int(char) ** key) % n) for char in cipher.split('#')])

    
    cipher = request.GET.get('cipher')
    key_pair = request.GET.get('key_pair').strip('()')

    passwords = {'cipher':cipher, 'original_password': get_original_password(cipher,key_pair)}

    return render(request, 'generator/decrypt.html', passwords)