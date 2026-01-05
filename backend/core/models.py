from django.db import models

# Create your models here.

#Defining my models (Create Classes first that I need for my data)

class Customer_Data(models.Model):

#CustomerUID
Customer_UID = models.UUIDField()
#Car Model
Car_Model = models.CharField()
#InsuranceCompany
Insurance = models.CharField()
#DateCreated
Date_Created = models.DateTimeField()
Last_Update = models.DateTimeField()

class RepairJob(models.Model):

# ----- PHASE 1 (ESTIMATE PHASE) ------
# #RepairJOBUID
RepairJob_UID = models.UUIDField()
#ImagesOfDamages
Images = models.ImageField()
#InitialEstimate
Estimate_Price = models.DecimalField()
#InitialEstimateDate
Estimate_Date = models.DateTimeField()
#EstimateOfPartsToBeUsed
Repair_Order = models.CharField()
#EstimateOfRepairs/Job to be done
Job_Order = models.CharField()

# ------- PHASE 2 (APPROVED PHASE) ------

#LOA Approved Price
Approved_Estimate = models.DecimalField()
#LOA Approved Repairs
Approved_Repair_Order = models.CharField()
Approved_Job_Order = models.CharField()
#Date of LOA Approval
LOA_Date = models.DateTimeField()

#------ PHASE 3 (GAP/DIFFERENCE) ----- 

@property
   def price_variance(self):
      if self.loa_approved_total:
           return self.loa_approved_total - self.initial_estimate_total
        return 0



class Status(models.Model):

#Create Category Choices of all status kinds
CATEGORY_CHOICES: [
    ('APPROVAL', 'LOA & INSURANCE'),
    ('PARTS', 'Parts Procurement'),
    ('REPAIR', 'Repair Shop Stage'),
    ('PICKUP', 'Releasing Stage'),
    ('BILLING', 'Insurance Claims'),
    ('DISMANTLE', 'Total Wreck'),
]


#category name
Category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#name/status
Status = models.CharField(max_length=50) #eg. "LOA REJECTED"
#color
color_code = models.CharField(max_length=7)

def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"

class Status_Log(models.Model):
     
repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name="history")
status = models.ForeignKey(Status, on_delete=models.CASCADE)
changed_at = models.DateTimeField(auto_now_add=True)
notes = models.TextField(blank=True) #"Parts are late"











