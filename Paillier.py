import time

from charm.schemes.pkenc.pkenc_paillier99 import Ciphertext
from charm.toolbox.integergroup import RSAGroup
from charm.toolbox.integergroup import lcm,integer,toInt
from charm.toolbox.PKEnc import PKEnc

debug = False

def __init__(self, ct, pk, key):
    dict.__init__(self, ct)
    self.pk, self.key = pk, key


def __add__(self, other):
    if type(other) == int:  # rhs must be Cipher
        lhs = dict.__getitem__(self, self.key)
        return Ciphertext({self.key: lhs * ((self.pk['g'] ** other) % self.pk['n2'])},
                          self.pk, self.key)
    else:  # neither are plain ints
        lhs = dict.__getitem__(self, self.key)
        rhs = dict.__getitem__(other, self.key)
    return Ciphertext({self.key: (lhs * rhs) % self.pk['n2']},
                      self.pk, self.key)


def __mul__(self, other):
    if type(other) == int:
        lhs = dict.__getitem__(self, self.key)
        return Ciphertext({self.key: (lhs ** other)}, self.pk, self.key)

def randomize(self, r):  # need to provide random value
    lhs = dict.__getitem__(self, self.key)
    rhs = (integer(r) ** self.pk['n']) % self.pk['n2']
    return Ciphertext({self.key: (lhs * rhs) % self.pk['n2']})

def __str__(self):
    value = dict.__str__(self)
    return value  # + ", pk =" + str(pk)


class Pai99(PKEnc):
    def __init__(self, groupObj):
        PKEnc.__init__(self)
        global group
        group = groupObj

    def L(self, u, n):
    # computes L(u) => ((u - 1) / n)
        U = integer(int(u) - 1)
        if int(U) == 0:
            return integer(0, n)
        return U / n

    def keygen(self, secparam=512):
        (p, q, n) = group.paramgen(secparam)
        lam = lcm(p - 1, q - 1)
        n2 = n ** 2
        print(int(n).bit_length())
        g = group.random(n2)
        g**123214
        u = (self.L(((g % n2) ** lam), n) % n) ** -1
        pk, sk = {'n': n, 'g': g, 'n2': n2}, {'lamda': lam, 'u': u}
        return (pk, sk)



    def encrypt(self, pk, m):
        g, n, n2 = pk['g'], pk['n'], pk['n2']
        r = group.random(pk['n'])
        c = ((g % n2) ** m) * ((r % n2) ** n)
        return Ciphertext({'c': c}, pk, 'c')


    def decrypt(self, pk, sk, ct):
        n, n2 = pk['n'], pk['n2']
        m = ((self.L(ct['c'] ** sk['lamda'], n) % n) * sk['u']) % n
        return toInt(m)


    def encode(self, modulus, message):
        # takes a string and represents as a bytes object
        elem = integer(message)
        return elem % modulus

    def decode(self, pk, element):
        pass


group = RSAGroup()
pai = Pai99(group)
(public_key, secret_key) = pai.keygen()

msg_1 = 12345678987654321
msg_2 = 12345761234123409
msg_3 = msg_1 + msg_2

cipher_1 = pai.encrypt(public_key, msg_1)
cipher_2 = pai.encrypt(public_key, msg_2)
cipher_3 = cipher_1 + cipher_2
decrypted_msg_3 = pai.decrypt(public_key, secret_key, cipher_3)

(p, q, n) = group.paramgen(secparam=512)
lam = lcm(p - 1, q - 1)
n2 = n ** 2
print(int(n).bit_length())
g1 = group.random(n2)
g2 = group.random(n2)

gm=0
ge=0
for i in range(1000):
    t1=time.perf_counter()
    g1*g2
    t2=time.perf_counter()
    g1**123141
    t3 = time.perf_counter()
    gm+=(t2-t1)
    ge+=(t3-t2)
print("Multiplication on G",gm,"ms")
print("Exponentiation on G",ge,"ms")