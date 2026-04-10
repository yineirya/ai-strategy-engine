class ValueModeler:
    def __init__(self, hourly_rate: int = 50):
        self.hourly_rate = hourly_rate # Average cost of a manual worker

    def calculate_roi(self, steps: list, volume_per_month: int):
        total_savings = 0
        total_cost = 0
        
        for step in steps:
            # Assume each manual step takes 15 mins (0.25 hrs)
            manual_time = 0.25 
            savings = volume_per_month * manual_time * self.hourly_rate
            
            # Assume AI cost is roughly $0.05 per transaction
            ai_cost = volume_per_month * 0.05
            
            total_savings += savings
            total_cost += ai_cost

        net_value = total_savings - total_cost
        roi_percentage = (net_value / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            "monthly_savings": total_savings,
            "monthly_cost": total_cost,
            "net_roi": f"{roi_percentage:.2f}%"
        }