
# =====================================================
# TOKEN-BASED AUTH vs JWT (Özet Tablo)
# =====================================================

# Özellik                | Token-Based Auth (Klasik) | JWT
# --------------------- | ------------------------- | ---------------------------
# Token saklama         | Veritabanında            | Saklanmaz (stateless)
# DB sorgusu gerekir mi | Evet                     | Hayır
# Token içeriği         | Anlamsız string           | User info + exp + imza
# Doğrulama yöntemi     | DB'den kontrol            | İmza doğrulama
# Logout / revoke       | Kolay (DB'den silinir)    | Zor (süre dolana kadar)
# Ölçeklenebilirlik     | Orta                      | Yüksek
# Performans            | DB'ye bağlı               | Daha hızlı
# Güvenlik riski        | Token sızıntısı DB ile iptal | Token süresi bitene kadar geçerli
# Kullanım alanı        | Küçük / kontrollü API     | SPA / Mobile / Microservice
# =====================================================

##############################################################################################

# =====================================================
# JWT (JSON Web Token) Yapısı – Kısa Not
# =====================================================

# JWT 3 parçadan oluşur:
# 1) Header
# 2) Payload
# 3) Signature

# -----------------------------------------------------
# 1) HEADER
# -----------------------------------------------------
# {
#   "alg": "HS256",
#   "typ": "JWT"
# }
#
# alg : Token'ın hangi algoritma ile imzalandığını söyler
#       (HS256 = HMAC + SHA256, secret key kullanır)
#
# typ : Token türü (JWT olduğunu belirtir)

# -----------------------------------------------------
# 2) PAYLOAD (Claims)
# -----------------------------------------------------
# {
#   "token_type": "access",
#   "exp": 1769449557,
#   "iat": 1769449257,
#   "jti": "171e0e223d354be9aebbd85e32dd4e61",
#   "user_id": "1"
# }
#
# token_type : Token'ın tipi (access / refresh)
# exp        : Token'ın sona erme zamanı (UNIX timestamp)
# iat        : Token'ın oluşturulma zamanı
# jti        : Token için benzersiz ID
# user_id    : Bu token'ın hangi kullanıcıya ait olduğu

# NOT:
# Payload içeriği GİZLİ DEĞİLDİR
# Base64 decode edilerek herkes tarafından okunabilir

# -----------------------------------------------------
# 3) SIGNATURE
# -----------------------------------------------------
# Signature = Header + Payload + SECRET KEY
#
# Amaç:
# - Token değiştirildi mi?
# - Bu token'ı gerçekten server mı üretti?

# jwt.io'da "signature verification failed" görmen normaldir
# Çünkü server'da kullanılan SECRET KEY jwt.io'da yok

# -----------------------------------------------------
# GENEL MANTIK (TEK CÜMLE)
# -----------------------------------------------------
# JWT = İçinde kullanıcı bilgisi taşıyan, imzalı ve süresi olan token
# =====================================================
