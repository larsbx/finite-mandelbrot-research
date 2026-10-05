# exact_type_irreducibility.mojo
#
# Irreducibility over Q of the exact-type polynomials of the critical orbit,
# certified by factor degrees modulo small primes.
#
# E_{ell,k} in Z[C] is the monic polynomial whose roots are the parameters of
# exact type (ell, k) (dynamics/critical_type_census.mojo). Over Z,
#
#   R_{ell,k} = Q_{ell+k} - Q_ell = E_{ell,k} * prod E_{mu,lambda}^{m}
#
# over the lower types mu <= ell, lambda | k, with the multiplicities m of
# multiplicities(). Every factor is monic, so the identity survives reduction
# modulo p and E_{ell,k} mod p is an exact quotient of polynomials over F_p.
#
# Certificate. At each listed prime, E mod p is squarefree with the listed
# factor degrees (distinct-degree factorization). If E = G H over Q, Gauss's
# lemma makes G and H monic in Z[C], so deg G is a subset sum of the factor
# degrees at every prime; E is irreducible when the common subset sums are
# {0, deg E}. The multiplicity read off by exact division is the true one only
# once the lower E are irreducible, so the types are certified in increasing
# order and a type is accepted only after every lower one.
#
# reference/python/polynomial/exact_type_irreducibility.py recomputes E over Z,
# the multiplicities by exact division, and every certificate with its own
# factorization; tests/test_exact_type_irreducibility.py binds the two.

comptime CERTIFIED_HORIZON = 8


@fieldwise_init
struct Multiplicity(ImplicitlyCopyable):
    var ell: Int
    var k: Int
    var mu: Int
    var lam: Int
    var m: Int


@fieldwise_init
struct FactorPattern(ImplicitlyCopyable):
    var ell: Int
    var k: Int
    var prime: Int
    var degrees: String


def multiplicities() -> List[Multiplicity]:
    return [
        Multiplicity(0, 2, 0, 1, 1),
        Multiplicity(2, 1, 0, 1, 3),
        Multiplicity(0, 3, 0, 1, 1),
        Multiplicity(3, 1, 0, 1, 4),
        Multiplicity(3, 1, 2, 1, 1),
        Multiplicity(2, 2, 0, 1, 3),
        Multiplicity(2, 2, 0, 2, 2),
        Multiplicity(2, 2, 2, 1, 1),
        Multiplicity(0, 4, 0, 1, 1),
        Multiplicity(0, 4, 0, 2, 1),
        Multiplicity(4, 1, 0, 1, 5),
        Multiplicity(4, 1, 2, 1, 1),
        Multiplicity(4, 1, 3, 1, 1),
        Multiplicity(3, 2, 0, 1, 4),
        Multiplicity(3, 2, 0, 2, 3),
        Multiplicity(3, 2, 2, 1, 1),
        Multiplicity(3, 2, 3, 1, 1),
        Multiplicity(3, 2, 2, 2, 1),
        Multiplicity(2, 3, 0, 1, 3),
        Multiplicity(2, 3, 2, 1, 1),
        Multiplicity(2, 3, 0, 3, 2),
        Multiplicity(0, 5, 0, 1, 1),
        Multiplicity(5, 1, 0, 1, 6),
        Multiplicity(5, 1, 2, 1, 1),
        Multiplicity(5, 1, 3, 1, 1),
        Multiplicity(5, 1, 4, 1, 1),
        Multiplicity(4, 2, 0, 1, 5),
        Multiplicity(4, 2, 0, 2, 3),
        Multiplicity(4, 2, 2, 1, 1),
        Multiplicity(4, 2, 3, 1, 1),
        Multiplicity(4, 2, 2, 2, 1),
        Multiplicity(4, 2, 4, 1, 1),
        Multiplicity(4, 2, 3, 2, 1),
        Multiplicity(3, 3, 0, 1, 4),
        Multiplicity(3, 3, 2, 1, 1),
        Multiplicity(3, 3, 0, 3, 2),
        Multiplicity(3, 3, 3, 1, 1),
        Multiplicity(3, 3, 2, 3, 1),
        Multiplicity(2, 4, 0, 1, 3),
        Multiplicity(2, 4, 0, 2, 2),
        Multiplicity(2, 4, 2, 1, 1),
        Multiplicity(2, 4, 2, 2, 1),
        Multiplicity(2, 4, 0, 4, 2),
        Multiplicity(0, 6, 0, 1, 1),
        Multiplicity(0, 6, 0, 2, 1),
        Multiplicity(0, 6, 0, 3, 1),
        Multiplicity(6, 1, 0, 1, 7),
        Multiplicity(6, 1, 2, 1, 1),
        Multiplicity(6, 1, 3, 1, 1),
        Multiplicity(6, 1, 4, 1, 1),
        Multiplicity(6, 1, 5, 1, 1),
        Multiplicity(5, 2, 0, 1, 6),
        Multiplicity(5, 2, 0, 2, 4),
        Multiplicity(5, 2, 2, 1, 1),
        Multiplicity(5, 2, 3, 1, 1),
        Multiplicity(5, 2, 2, 2, 1),
        Multiplicity(5, 2, 4, 1, 1),
        Multiplicity(5, 2, 3, 2, 1),
        Multiplicity(5, 2, 5, 1, 1),
        Multiplicity(5, 2, 4, 2, 1),
        Multiplicity(4, 3, 0, 1, 5),
        Multiplicity(4, 3, 2, 1, 1),
        Multiplicity(4, 3, 0, 3, 3),
        Multiplicity(4, 3, 3, 1, 1),
        Multiplicity(4, 3, 4, 1, 1),
        Multiplicity(4, 3, 2, 3, 1),
        Multiplicity(4, 3, 3, 3, 1),
        Multiplicity(3, 4, 0, 1, 4),
        Multiplicity(3, 4, 0, 2, 3),
        Multiplicity(3, 4, 2, 1, 1),
        Multiplicity(3, 4, 3, 1, 1),
        Multiplicity(3, 4, 2, 2, 1),
        Multiplicity(3, 4, 0, 4, 2),
        Multiplicity(3, 4, 3, 2, 1),
        Multiplicity(3, 4, 2, 4, 1),
        Multiplicity(2, 5, 0, 1, 3),
        Multiplicity(2, 5, 2, 1, 1),
        Multiplicity(2, 5, 0, 5, 2),
        Multiplicity(0, 7, 0, 1, 1),
        Multiplicity(7, 1, 0, 1, 8),
        Multiplicity(7, 1, 2, 1, 1),
        Multiplicity(7, 1, 3, 1, 1),
        Multiplicity(7, 1, 4, 1, 1),
        Multiplicity(7, 1, 5, 1, 1),
        Multiplicity(7, 1, 6, 1, 1),
        Multiplicity(6, 2, 0, 1, 7),
        Multiplicity(6, 2, 0, 2, 4),
        Multiplicity(6, 2, 2, 1, 1),
        Multiplicity(6, 2, 3, 1, 1),
        Multiplicity(6, 2, 2, 2, 1),
        Multiplicity(6, 2, 4, 1, 1),
        Multiplicity(6, 2, 3, 2, 1),
        Multiplicity(6, 2, 5, 1, 1),
        Multiplicity(6, 2, 4, 2, 1),
        Multiplicity(6, 2, 6, 1, 1),
        Multiplicity(6, 2, 5, 2, 1),
        Multiplicity(5, 3, 0, 1, 6),
        Multiplicity(5, 3, 2, 1, 1),
        Multiplicity(5, 3, 0, 3, 3),
        Multiplicity(5, 3, 3, 1, 1),
        Multiplicity(5, 3, 4, 1, 1),
        Multiplicity(5, 3, 2, 3, 1),
        Multiplicity(5, 3, 5, 1, 1),
        Multiplicity(5, 3, 3, 3, 1),
        Multiplicity(5, 3, 4, 3, 1),
        Multiplicity(4, 4, 0, 1, 5),
        Multiplicity(4, 4, 0, 2, 3),
        Multiplicity(4, 4, 2, 1, 1),
        Multiplicity(4, 4, 3, 1, 1),
        Multiplicity(4, 4, 2, 2, 1),
        Multiplicity(4, 4, 0, 4, 2),
        Multiplicity(4, 4, 4, 1, 1),
        Multiplicity(4, 4, 3, 2, 1),
        Multiplicity(4, 4, 4, 2, 1),
        Multiplicity(4, 4, 2, 4, 1),
        Multiplicity(4, 4, 3, 4, 1),
        Multiplicity(3, 5, 0, 1, 4),
        Multiplicity(3, 5, 2, 1, 1),
        Multiplicity(3, 5, 3, 1, 1),
        Multiplicity(3, 5, 0, 5, 2),
        Multiplicity(3, 5, 2, 5, 1),
        Multiplicity(2, 6, 0, 1, 3),
        Multiplicity(2, 6, 0, 2, 2),
        Multiplicity(2, 6, 2, 1, 1),
        Multiplicity(2, 6, 0, 3, 2),
        Multiplicity(2, 6, 2, 2, 1),
        Multiplicity(2, 6, 2, 3, 1),
        Multiplicity(2, 6, 0, 6, 2),
        Multiplicity(0, 8, 0, 1, 1),
        Multiplicity(0, 8, 0, 2, 1),
        Multiplicity(0, 8, 0, 4, 1),
    ]


def certificates() -> List[FactorPattern]:
    return [
        FactorPattern(0, 3, 3, "3"),
        FactorPattern(3, 1, 3, "3"),
        FactorPattern(2, 2, 3, "2"),
        FactorPattern(0, 4, 3, "6"),
        FactorPattern(4, 1, 3, "2 5"),
        FactorPattern(4, 1, 5, "3 4"),
        FactorPattern(3, 2, 3, "3"),
        FactorPattern(2, 3, 3, "1 5"),
        FactorPattern(2, 3, 5, "6"),
        FactorPattern(0, 5, 3, "5 10"),
        FactorPattern(0, 5, 5, "2 13"),
        FactorPattern(5, 1, 3, "15"),
        FactorPattern(4, 2, 3, "3 5"),
        FactorPattern(4, 2, 5, "8"),
        FactorPattern(3, 3, 3, "2 10"),
        FactorPattern(3, 3, 7, "3 9"),
        FactorPattern(2, 4, 3, "3 9"),
        FactorPattern(2, 4, 7, "12"),
        FactorPattern(0, 6, 3, "6 8 13"),
        FactorPattern(0, 6, 5, "6 10 11"),
        FactorPattern(0, 6, 7, "2 3 22"),
        FactorPattern(6, 1, 3, "10 21"),
        FactorPattern(6, 1, 7, "4 12 15"),
        FactorPattern(5, 2, 3, "4 5 6"),
        FactorPattern(5, 2, 5, "3 12"),
        FactorPattern(4, 3, 3, "4 17"),
        FactorPattern(4, 3, 5, "8 13"),
        FactorPattern(3, 4, 3, "10 14"),
        FactorPattern(3, 4, 7, "1 23"),
        FactorPattern(2, 5, 3, "7 23"),
        FactorPattern(2, 5, 11, "1 3 26"),
        FactorPattern(0, 7, 3, "13 50"),
        FactorPattern(0, 7, 5, "11 19 33"),
        FactorPattern(7, 1, 3, "7 15 41"),
        FactorPattern(7, 1, 5, "2 3 58"),
        FactorPattern(6, 2, 3, "16 16"),
        FactorPattern(6, 2, 5, "2 8 9 13"),
        FactorPattern(5, 3, 3, "3 9 11 25"),
        FactorPattern(5, 3, 7, "6 42"),
        FactorPattern(4, 4, 3, "11 37"),
        FactorPattern(4, 4, 5, "48"),
        FactorPattern(3, 5, 3, "13 14 33"),
        FactorPattern(3, 5, 5, "7 7 12 17 17"),
        FactorPattern(3, 5, 7, "60"),
        FactorPattern(2, 6, 3, "54"),
        FactorPattern(0, 8, 3, "22 48 50"),
        FactorPattern(0, 8, 5, "29 91"),
    ]


def trim(var a: List[Int]) -> List[Int]:
    while len(a) > 1 and a[len(a) - 1] == 0:
        _ = a.pop()
    if len(a) == 0:
        a.append(0)
    return a^


def inverse(a: Int, p: Int) -> Int:
    var result = 1
    var base = a % p
    var e = p - 2
    while e > 0:
        if e % 2 == 1:
            result = result * base % p
        base = base * base % p
        e //= 2
    return result


def mul(a: List[Int], b: List[Int], p: Int) -> List[Int]:
    var out = List[Int](length=len(a) + len(b) - 1, fill=0)
    for i in range(len(a)):
        if a[i] != 0:
            for j in range(len(b)):
                out[i + j] = (out[i + j] + a[i] * b[j]) % p
    return trim(out^)


def divide(a: List[Int], b: List[Int], p: Int) -> Tuple[List[Int], List[Int]]:
    """Quotient and remainder over F_p; b nonzero."""
    var r = List[Int](capacity=len(a))
    for x in a:
        r.append(x % p)
    var db = len(b) - 1
    var lead = inverse(b[db], p)
    var q = List[Int](length=max(len(a) - db, 1), fill=0)
    for i in range(len(a) - 1 - db, -1, -1):
        var c = r[i + db] * lead % p
        q[i] = c
        if c != 0:
            for j in range(db + 1):
                r[i + j] = (r[i + j] - c * b[j] % p + p) % p
    var rem = List[Int](capacity=max(db, 1))
    for i in range(db):
        rem.append(r[i] if i < len(r) else 0)
    return (trim(q^), trim(rem^))


def quotient(a: List[Int], b: List[Int], p: Int) -> List[Int]:
    return divide(a, b, p)[0].copy()


def remainder(a: List[Int], b: List[Int], p: Int) -> List[Int]:
    return divide(a, b, p)[1].copy()


def gcd(a: List[Int], b: List[Int], p: Int) -> List[Int]:
    var x = trim(a.copy())
    var y = trim(b.copy())
    while not (len(y) == 1 and y[0] == 0):
        var r = remainder(x, y, p)
        x = y^
        y = r^
    return x^


def relation_mod_p(ell: Int, k: Int, p: Int) -> List[Int]:
    var c = List[Int]()
    c.append(0)
    c.append(1)
    var q = List[Int]()
    q.append(0)
    var q_ell = q.copy()
    for n in range(ell + k):
        if n == ell:
            q_ell = q.copy()
        var s = mul(q, q, p)
        s = trim(s^)
        while len(s) < 2:
            s.append(0)
        s[1] = (s[1] + 1) % p
        q = trim(s^)
    var out = List[Int](length=max(len(q), len(q_ell)), fill=0)
    for i in range(len(q)):
        out[i] = q[i]
    for i in range(len(q_ell)):
        out[i] = (out[i] - q_ell[i] + p) % p
    return trim(out^)


def exact_type_mod_p(ell: Int, k: Int, p: Int) raises -> List[Int]:
    """E_{ell,k} mod p as the exact quotient of R_{ell,k}; raises if a division is not exact."""
    var rest = relation_mod_p(ell, k, p)
    for row in multiplicities():
        if row.ell == ell and row.k == k:
            var lower = exact_type_mod_p(row.mu, row.lam, p)
            for _ in range(row.m):
                var qr = divide(rest, lower, p)
                if not (len(qr[1]) == 1 and qr[1][0] == 0):
                    raise Error("inexact division of R_" + String(ell) + "," + String(k))
                rest = qr[0].copy()
    return rest^


def factor_degrees(f: List[Int], p: Int) raises -> List[Int]:
    """Sorted factor degrees of monic f mod p (p < 2^31); raises when f mod p is not squarefree."""
    var d = len(f) - 1
    var df = List[Int](capacity=d)
    for i in range(1, d + 1):
        df.append(i * f[i] % p)
    if len(gcd(f, trim(df^), p)) != 1:
        raise Error("not squarefree")
    var x = List[Int]()
    x.append(0)
    x.append(1)
    var xp = List[Int]()
    xp.append(1)
    var base = remainder(x, f, p)
    var e = p
    while e > 0:
        if e % 2 == 1:
            xp = remainder(mul(xp, base, p), f, p)
        base = remainder(mul(base, base, p), f, p)
        e //= 2
    var frobenius = List[List[Int]]()
    var one = List[Int]()
    one.append(1)
    frobenius.append(one^)
    for j in range(1, d):
        frobenius.append(remainder(mul(frobenius[j - 1], xp, p), f, p))
    var degrees = List[Int]()
    var g = f.copy()
    var h = x.copy()
    var i = 0
    while len(g) - 1 >= 2 * (i + 1):
        i += 1
        var next = List[Int](length=d, fill=0)
        for j in range(len(h)):
            if h[j] != 0:
                for t in range(len(frobenius[j])):
                    next[t] = (next[t] + h[j] * frobenius[j][t]) % p
        h = trim(next^)
        var diff = h.copy()
        while len(diff) < 2:
            diff.append(0)
        diff[1] = (diff[1] - 1 + p) % p
        var common = gcd(g, trim(diff^), p)
        if len(common) > 1:
            for _ in range((len(common) - 1) // i):
                degrees.append(i)
            g = quotient(g, common, p)
    if len(g) > 1:
        degrees.append(len(g) - 1)
    sort(degrees)
    return degrees^


def parse_degrees(s: String) raises -> List[Int]:
    var out = List[Int]()
    for part in s.split(" "):
        out.append(Int(String(part)))
    return out^


def forces_irreducible(degree: Int, patterns: List[List[Int]]) -> Bool:
    """True iff the only subset sums common to every factor-degree pattern are 0 and degree."""
    var common = List[Bool](length=degree + 1, fill=True)
    for degrees in patterns:
        var reach = List[Bool](length=degree + 1, fill=False)
        reach[0] = True
        var total = 0
        for d in degrees:
            total += d
            for s in range(degree, d - 1, -1):
                if reach[s - d]:
                    reach[s] = True
        if total != degree:
            return False
        for s in range(degree + 1):
            common[s] = common[s] and reach[s]
    for s in range(1, degree):
        if common[s]:
            return False
    return True


def certified_irreducible(ell: Int, k: Int, patterns: List[FactorPattern]) raises -> Bool:
    """Replays the listed factor patterns of E_{ell,k}; True iff they force irreducibility."""
    var degree = len(exact_type_mod_p(ell, k, 3)) - 1
    var replayed = List[List[Int]]()
    for row in patterns:
        if row.ell != ell or row.k != k:
            continue
        var f = exact_type_mod_p(ell, k, row.prime)
        if len(f) - 1 != degree:
            return False
        var degrees = factor_degrees(f, row.prime)
        var claimed = parse_degrees(row.degrees)
        if len(degrees) != len(claimed):
            return False
        for t in range(len(degrees)):
            if degrees[t] != claimed[t]:
                return False
        replayed.append(degrees^)
    return forces_irreducible(degree, replayed)


def all_types_certified(patterns: List[FactorPattern]) raises -> Bool:
    """Every exact type with ell + k <= CERTIFIED_HORIZON, in increasing order."""
    for horizon in range(1, CERTIFIED_HORIZON + 1):
        for k in range(1, horizon + 1):
            var ell = horizon - k
            if ell != 1 and not certified_irreducible(ell, k, patterns):
                return False
    return True


def exact_type_irreducibility_smoke() -> Bool:
    try:
        if not all_types_certified(certificates()):
            return False
        # A product of two exact-type polynomials must never certify.
        var product_patterns = List[List[Int]]()
        for p in [3, 5, 7, 11, 13, 17, 19, 23]:
            var product = mul(exact_type_mod_p(0, 3, p), exact_type_mod_p(3, 1, p), p)
            try:
                product_patterns.append(factor_degrees(product, p))
            except:
                pass
        if len(product_patterns) < 3 or forces_irreducible(6, product_patterns):
            return False
        # Every factor pattern sums to its degree and counts the roots mod p.
        for row in certificates():
            var f = exact_type_mod_p(row.ell, row.k, row.prime)
            var degrees = factor_degrees(f, row.prime)
            var linear = 0
            for d in degrees:
                if d == 1:
                    linear += 1
            var roots = 0
            for c in range(row.prime):
                var acc = 0
                for i in range(len(f) - 1, -1, -1):
                    acc = (acc * c + f[i]) % row.prime
                if acc == 0:
                    roots += 1
            if roots != linear:
                return False
        return True
    except:
        return False
