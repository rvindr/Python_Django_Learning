from django.shortcuts import render, redirect
from tracker.mongo_client import expense_coll
from django.views import View
from tracker.serializers import ExpenseSerializer
from django.contrib import messages
from bson import ObjectId  




class ExpenseView(View):

    def get(self, request):
        transactions = list(expense_coll.find())

        for transaction in transactions:
            transaction['id'] = str(transaction['_id'])  

        aggregation_pipeline = [
            {
                "$group": {
                    "_id": None,
                    "totalAmount": {"$sum": "$amount"},
                    "totalIncome": {"$sum": {"$cond": {"if": {"$gte": ["$amount", 0]}, "then": "$amount", "else": 0}}},
                    "totalExpenses": {"$sum": {"$cond": {"if": {"$lt": ["$amount", 0]}, "then": "$amount", "else": 0}}}
                }
            }
        ]

        result = list(expense_coll.aggregate(aggregation_pipeline))

        if result:
            total_amount = result[0]['totalAmount']
            total_income = result[0]['totalIncome']
            total_expenses = -result[0]['totalExpenses']  
        else:
            total_amount = 0
            total_income = 0
            total_expenses = 0

        return render(request, 'home.html', {
            'transactions': transactions,
            'total_amount': total_amount,
            'total_income': total_income,
            'total_expenses': total_expenses
        })
    
    def post(self, request):
        data = {
            'description': request.POST.get('desc'),
            'amount': float(request.POST.get('amount')) 
        }


        serializer = ExpenseSerializer(data=data)

        if serializer.is_valid():
            expense_coll.insert_one(serializer.validated_data)
            messages.success(request, "Expense added successfully!")
        else:
            messages.error(request, "Error adding expense: " + str(serializer.errors))


        return redirect('expense_view')


class DeleteExpenseView(View):
    
    def post(self, request, expense_id):
        try:
            obj_id = ObjectId(expense_id)
        except Exception as e:
            messages.error(request, "Invalid expense ID.")
            return redirect('expense_view')
        
        result = expense_coll.delete_one({"_id": obj_id})
        
        if result.deleted_count > 0:
            messages.success(request, "Expense deleted successfully!")
        else:
            messages.error(request, "Expense not found!")
        
        return redirect('expense_view')