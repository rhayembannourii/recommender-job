# from email.message import EmailMessage
# import ssl
# import smtplib
#
#
# def send_test():
#     email_sender = "rhayembannouri1@gmail.com"
#     email_password = "tqfxsyzutdzwugjr"
#     email_receiver = "rhayembannouri5@gmail.com"
#
#     subject = "Your Python test"
#     body = """
#     Question 1/5 : Python
#     Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
#
#
#     n = 0
#     while n<15 :
#         n = n + 2
#     print(n)
#
#     Qu'affiche le script ?
#
#     Je ne sais pas
#     A) 14
#     B) 15
#     C) 16
#     D) 17
#
#
#     Question 2/5 : Python
#
#     Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
#
#
#     n = 10
#     while n>=11 :
#         n = n + 2
#     print(n)
#
#     Qu'affiche le script ?
#
#     Je ne sais pas
#     A) 10
#     B) 11
#     C) 12
#     D) 13
#
#     Question 3/5 : Python
#
#     Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
#
#
#     n = 0
#     for i in range(5) :
#         n = n + 1
#     print(n)
#
#     Qu'affiche le script ?
#
#     Je ne sais pas
#     A) 4
#     B) 5
#     C) 6
#     D) 7
#
#     Question 4/5 : Python
#
#     Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
#
#
#     n = 0
#     for i in range(5) :
#         n = n + 1
#     print(i)
#
#     Qu'affiche le script ?
#
#     Je ne sais pas
#     A) 4
#     B) 5
#     C) 6
#     D) 7
#
#     Question 5/5 : Python
#
#     Barème : bonne réponse 4 points, mauvaise réponse -1 point, je ne sais pas 0 point
#
#
#     resultat = ""
#     for c in "Bonsoir" :
#         resultat = resultat + c
#     print(resultat)
#
#     Qu'affiche le script ?
#
#     Je ne sais pas
#     A) Bonsoir
#     B) riosnoB
#     C) BonsoirBonsoirBonsoirBonsoirBonsoirBonsoirBonsoir
#
#
#     """
#
#     em = EmailMessage()
#     em['From'] = email_sender
#     em['To'] = email_receiver
#     em['Subject'] = subject
#     em.set_content(body)
#
#     context = ssl.create_default_context()
#
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(email_sender, email_password)
#         smtp.sendmail(email_sender, email_receiver, em.as_string())
#
# send_test()