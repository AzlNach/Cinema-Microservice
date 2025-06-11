from graphene import ObjectType, String, Int, Float, List, Field, Mutation, Schema, Boolean
from models import Payment, db
from datetime import datetime
import traceback

class PaymentType(ObjectType):
    id = Int()
    userId = Int()
    bookingId = Int()
    amount = Float()
    paymentMethod = String()
    status = String()  # pending, success, failed
    paymentProofImage = String()
    createdAt = String()
    updatedAt = String()
    canBeDeleted = Boolean()
    
    def resolve_userId(self, info):
        return self.user_id if hasattr(self, 'user_id') else getattr(self, 'userId', None)
    
    def resolve_bookingId(self, info):
        return self.booking_id if hasattr(self, 'booking_id') else getattr(self, 'bookingId', None)
        
    def resolve_paymentMethod(self, info):
        return self.payment_method if hasattr(self, 'payment_method') else getattr(self, 'paymentMethod', None)
        
    def resolve_paymentProofImage(self, info):
        return self.payment_proof_image if hasattr(self, 'payment_proof_image') else getattr(self, 'paymentProofImage', None)
        
    def resolve_createdAt(self, info):
        if hasattr(self, 'created_at') and self.created_at:
            return self.created_at.isoformat()
        return getattr(self, 'createdAt', None)
        
    def resolve_updatedAt(self, info):
        if hasattr(self, 'updated_at') and self.updated_at:
            return self.updated_at.isoformat()
        return getattr(self, 'updatedAt', None)
    
    def resolve_canBeDeleted(self, info):
        if hasattr(self, 'can_be_deleted_by_user'):
            return self.can_be_deleted_by_user()
        return False

class UpdatePaymentStatusResponse(ObjectType):
    payment = Field(PaymentType)
    success = Boolean()
    message = String()

class UpdatePaymentStatus(Mutation):
    class Arguments:
        id = Int(required=True)
        status = String(required=True)  # pending, success, failed

    Output = UpdatePaymentStatusResponse

    def mutate(self, info, id, status):
        try:
            # Validate status
            valid_statuses = ['pending', 'success', 'failed']
            if status not in valid_statuses:
                return UpdatePaymentStatusResponse(
                    payment=None,
                    success=False,
                    message=f"Invalid status '{status}'. Valid statuses are: {', '.join(valid_statuses)}"
                )

            payment = Payment.query.get(id)
            if not payment:
                return UpdatePaymentStatusResponse(
                    payment=None,
                    success=False,
                    message=f"Payment with ID {id} not found"
                )

            old_status = payment.status
            payment.status = status
            payment.save()

            return UpdatePaymentStatusResponse(
                payment=payment,
                success=True,
                message=f"Payment status updated from '{old_status}' to '{status}'"
            )
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            return UpdatePaymentStatusResponse(
                payment=None,
                success=False,
                message=f"Error updating payment status: {str(e)}"
            )
            
class CreatePaymentResponse(ObjectType):
    payment = Field(PaymentType)
    success = Boolean()
    message = String()

class CreatePayment(Mutation):
    class Arguments:
        user_id = Int(required=True)
        booking_id = Int(required=True)
        amount = Float(required=True)  # CHANGED: This will be final amount after discount
        payment_method = String(required=True)
        payment_proof_image = String()

    Output = CreatePaymentResponse

    def mutate(self, info, user_id, booking_id, amount, payment_method, payment_proof_image=None):
        try:
            print(f"DEBUG: Creating payment - user_id: {user_id}, booking_id: {booking_id}, amount: {amount}")
            
            # Check if payment already exists for this booking
            existing_payment = Payment.query.filter_by(booking_id=booking_id).first()
            if existing_payment:
                return CreatePaymentResponse(
                    payment=None,
                    success=False,
                    message="Payment already exists for this booking"
                )

            # UPDATED: Use the provided amount directly (this is already the final amount after discount)
            final_amount = float(amount)
            print(f"DEBUG: Final amount to be stored: {final_amount}")

            # Create payment with the final amount
            payment = Payment(
                user_id=user_id,
                booking_id=booking_id,
                amount=final_amount,  # Store the discounted amount
                payment_method=payment_method,
                status='PAID',  # Set as paid immediately for demo
                payment_proof_image=payment_proof_image,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            payment.save()
            print(f"DEBUG: Payment created successfully with ID: {payment.id}, Amount: {payment.amount}")

            return CreatePaymentResponse(
                payment=payment,
                success=True,
                message=f"Payment of ${final_amount:.2f} created successfully"
            )
        except Exception as e:
            db.session.rollback()
            print(f"DEBUG: Error creating payment: {str(e)}")
            traceback.print_exc()
            return CreatePaymentResponse(
                payment=None,
                success=False,
                message=f"Error creating payment: {str(e)}"
            )

class UpdatePaymentResponse(ObjectType):
    payment = Field(PaymentType)
    success = Boolean()
    message = String()

class UpdatePayment(Mutation):
    class Arguments:
        id = Int(required=True)
        status = String()
        payment_proof_image = String()

    Output = UpdatePaymentResponse

    def mutate(self, info, id, status=None, payment_proof_image=None):
        try:
            payment = Payment.query.get(id)
            if not payment:
                return UpdatePaymentResponse(
                    payment=None,
                    success=False,
                    message=f"Payment with ID {id} not found"
                )
            
            if status:
                payment.status = status
            if payment_proof_image:
                payment.payment_proof_image = payment_proof_image
                
            payment.save()
            
            return UpdatePaymentResponse(
                payment=payment,
                success=True,
                message="Payment updated successfully"
            )
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            return UpdatePaymentResponse(
                payment=None,
                success=False,
                message=f"Error updating payment: {str(e)}"
            )

class DeletePaymentResponse(ObjectType):
    success = Boolean()
    message = String()

class DeletePayment(Mutation):
    class Arguments:
        id = Int(required=True)

    Output = DeletePaymentResponse

    def mutate(self, info, id):
        try:
            payment = Payment.query.get(id)
            if not payment:
                return DeletePaymentResponse(
                    success=False,
                    message=f"Payment with ID {id} not found"
                )
            
            if not payment.can_be_deleted:
                return DeletePaymentResponse(
                    success=False,
                    message="This payment cannot be deleted"
                )
            
            payment.delete()
            return DeletePaymentResponse(
                success=True,
                message="Payment deleted successfully"
            )
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            return DeletePaymentResponse(
                success=False,
                message=f"Error deleting payment: {str(e)}"
            )

class Query(ObjectType):
    payments = List(PaymentType)
    payment = Field(PaymentType, id=Int(required=True))
    user_payments = List(PaymentType, userId=Int(required=True))  # ← Changed from user_id to userId
    pending_payments = List(PaymentType)
    expired_payments = List(PaymentType)

    def resolve_payments(self, info):
        try:
            return Payment.query.all()
        except Exception as e:
            print(f"Error in resolve_payments: {str(e)}")
            traceback.print_exc()
            return []
        
    def resolve_payment(self, info, id):
        try:
            return Payment.query.get(id)
        except Exception as e:
            print(f"Error in resolve_payment: {str(e)}")
            return None
    
    def resolve_user_payments(self, info, userId):
        try:
            payments = Payment.query.filter(Payment.user_id == userId).all()
            print(f"Found {len(payments)} payments for user {userId}")
            for payment in payments:
                print(f"Payment {payment.id}: booking_id={payment.booking_id}, user_id={payment.user_id}")
            return payments
        except Exception as e:
            print(f"Error in resolve_user_payments: {str(e)}")
            traceback.print_exc()
            return []
    
    def resolve_pending_payments(self, info):
        try:
            return Payment.query.filter_by(status='pending').all()
        except Exception as e:
            print(f"Error in resolve_pending_payments: {str(e)}")
            traceback.print_exc()
            return []
    
    def resolve_expired_payments(self, info):
        try:
            all_pending = Payment.query.filter_by(status='pending').all()
            expired = [p for p in all_pending if hasattr(p, 'is_expired') and p.is_expired()]
            return expired
        except Exception as e:
            print(f"Error in resolve_expired_payments: {str(e)}")
            traceback.print_exc()
            return []

class Mutation(ObjectType):
    create_payment = CreatePayment.Field()
    updatePaymentStatus = UpdatePaymentStatus.Field()
    update_payment = UpdatePayment.Field()
    delete_payment = DeletePayment.Field()

schema = Schema(query=Query, mutation=Mutation)