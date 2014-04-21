from django.shortcuts import render

# Create your views here.

#@login_required(login_url='/aep/login')
def index(request):
    # Use SQL Query to acquire user Company
    #cursor = connection.cursor()
    # this query returns two items : scalar and company ID
    #cursor.execute('select company_id, company_name from vlm_user_summary_view where id = %s', [request.user.id])
    #row = cursor.fetchone()
    #if row:
    #    company_id=row[0]  # column 0 is company
    #    userCompany=row[1] # column 1 is company name
    #    return render(request, 'index.html', {'userInfo':request.user, 'userCompany':userCompany,'company_id':company_id})
    return render(request, 'index.html', {'userInfo':'cure'})
