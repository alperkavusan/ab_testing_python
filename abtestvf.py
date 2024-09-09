#####################################################
# AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################
import pandas as pd

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
dfk=pd.read_excel("datasets/ab_testing.xlsx")
dft=pd.read_excel("datasets/ab_testing.xlsx",sheet_name=1)
dfk.head()
dft.head()
# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
dfk.describe().T
dft.describe().T
sms.DescrStatsW(dft["Purchase"]).tconfint_mean()
sms.DescrStatsW(dfk["Purchase"]).tconfint_mean()
# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.
dfk["group"]="Kontrol"
dft["group"]="Test"
df=pd.concat([dfk,dft],ignore_index=True)
df.head()
df.describe().T

dfk["Purchase"].corr(dft["Purchase"])
dfk["Purchase"].corr(dfk["Click"])
dfk["Impression"].corr(dfk["Click"])
#####################################################
# 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.


#  H0 : M1 = M2
#  H1 : M1!= M2

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

sms.DescrStatsW(dfk["Purchase"]).tconfint_mean()
sms.DescrStatsW(dft["Purchase"]).tconfint_mean()

dfk["Purchase"].mean()
dft["Purchase"].mean()
df.groupby("group").agg({"Purchase":"mean"})
#####################################################
# 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################



######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

test_stat, pvalue = shapiro(df.loc[df["group"] == "Kontrol", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
test_stat, pvalue = shapiro(df.loc[df["group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Shapiro testinde H0 : Normal dğılıyor der, red edemiyoruz yani iki grupta normal dağılıyor.
#Sıra levene testinde varyans homojen mi?

test_stat, pvalue = levene(df.loc[df["group"] == "Kontrol", "Purchase"],
                           df.loc[df["group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 varyanslar homojen der p value ya göre bunu da red edemiyoruz dolayısıyla varyanslar da homojen.



# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

#  Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "Kontrol", "Purchase"],
                              df.loc[df["group"] == "Test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 kontrol ve test grubunun yani max bid ile average bid grubunun ortalamaları arasında fark olmadığıydı.
# alpha 0.05 için H0 red edilemez yani ortalamalar birbirinden istatistiksel olarak farklıdır diyemiyoruz.

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

#Anlamlı fark yoktur.


##############################################################
# 4 : Sonuçların Analizi
##############################################################


#Varsayımlar sağlandığından ötürü parametrik t testini kullandık.


# Diğer verilerinde incelenmesi gerekebilir. Bu sayede hangi sebeple anlamlı farkın oluşmadığı gözlemlenebilir.