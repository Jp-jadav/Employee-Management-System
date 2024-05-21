from django.shortcuts import render,HttpResponse # type: ignore
from .models import Employee, Role, Department
import datetime
from django.db.models import Q # type: ignore

# Create your views here.
def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    print(context)
    return render(request,'view_all_emp.html',context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST.get('last_name', '').strip()
        salary = request.POST.get('salary', '').strip()
        phone = request.POST.get('phone', '').strip()
        bonus = request.POST.get('bonus', '').strip()
        dept_id = request.POST.get('dept', '').strip()
        role_id = request.POST.get('role', '').strip()
        
        # Validate required fields
        if not all([first_name, last_name, salary, phone, bonus, dept_id, role_id]):
            return HttpResponse("All fields are required.", status=400)
        
        try:
            salary = int(salary)
            phone = int(phone)
            bonus = int(bonus)
            dept_id = int(dept_id)
            role_id = int(role_id)
        except ValueError:
            return HttpResponse("Invalid input for salary, phone, bonus, dept, or role. They must be integers.", status=400)

        # Fetch the Department and Role instances
        try:
            dept = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
        except Department.DoesNotExist:
            return HttpResponse("Department not found.", status=404)
        except Role.DoesNotExist:
            return HttpResponse("Role not found.", status=404)

        new_emp = Employee(
            firstname=first_name,
            lastname=last_name,
            dept=dept,  # Use the field name directly
            salary=salary,
            bonus=bonus,
            role=role,  # Use the field name directly
            phone=phone,
            hire_date=datetime.datetime.now()
        )
        new_emp.save()
        return HttpResponse("Employee added successfully...")
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception occurred! Employee has not been added.", status=405)
    
def remove_emp(request,emp_id = 0):
    if emp_id :
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Successfully removed.")
        except:
            return HttpResponse("Please Enter Valid EMP Id")
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    print(context)
    return render(request,'remove_emp.html',context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(firstname__icontains = name) | Q(lastname__icontains = name))
        elif dept:
            emps = emps.filter(dept__name = dept)
        elif role:
            emps = emps.filter(role__name = role)
        context ={
            'emps':emps
        }
        return render(request, 'view_all_emp.html', context) 
            
    elif request.method == 'GET':
        return render(request,'filter_emp.html')
    else:
        return HttpResponse("An Exception occurred ")