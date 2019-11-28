# EntryManagement
This is an entry management software made which keeps track of the visitor information in an organisation.
Whenever a persn visit the organization and enter his and his host detail , it trigger a mail and sms to host .
When he leaves, an email and sms is send to the visitor.

Technology Used : 
	FrontEnd technology - HTML,CSS,Semantic-UI,Javascript
	BackEnd Technology - Python ,Django Framework,SQlite

URL and pages :
	1. mainpage : http://127.0.0.1:8000/
	2. checkin page - http://127.0.0.1:8000/checkin 
	3. checkout page - http://127.0.0.1:8000/checkout
	4. Admin panel - http://127.0.0.1:8000/admin 
	
Logic Used:
1. The mainpage consist of button "checkIn" and "checkout"  which upon click leads to checkin and checkout page respectively.
	
CheckIn Logic :

for checkIn ,the User is provided with form which consist of details of host and visitor. Upon submission ,
1. we first check if the user is already checkIn and had not checkOut yet.
In that case, we redirect userto checkIn page with appropriate message like "You are already checkedIn".

2. If user is not checkedIn, we sent mai and sms to the user. If it is successful then,we create object of "MEETING " database            model .The Meeting model consist of all detail and one more boolean field "isCheckOut" which is set to False .This Field is              used for checkout alongwith visitor's emailId.When user checkout this Filed is set to True. After that we redirect it to the             mainpage with success message . For this ,session is created.		
	
CheckOut Logic :
for checkout,we asked visitor for checkIn email Id . we make use of isCheckOut field of Meeting Model.
isCheckOut was initially false . So we search for Meeting object with given email as guestemail and isCheckOut=False.
Two cases arises:

1. If there exist a object,it means user is checkedIn and we check him out by setting isCheckOut=Trueand send himt o the main with        success message.

2. No object is found,in that case user is not checkedIn . So we send user back to the checkout page with error message like "user       didn't checked". 
	
2. Also there is an admin panel from where the admin of the organization can make changes to the databsae 
when required.It requires userId and password to have access to it.
	
3. I haven't provide the priavte details like credential of sms and email services.
The whole project is fully commented for better understanding.
	   
