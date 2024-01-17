class Volunteer < ApplicationRecord
    # changes primary key
    self.primary_key = 'association_volunteer_id'
    
    def universal_requiremen
    
    end

    ##
    # First demo of compliance not used    
    #def is_8u_compliant?
    #    required_admin_cert_names = ["SafeSport", "Concussion Awareness", "Sudden Cardiac Arrest"]
        
        # Fetch all admin details for this volunteer and check for required certifications
   #     admin_cert_names = AdminDetail.where(admin_id: association_volunteer_id).pluck(:cert_name)
   #     has_required_admin_certs = required_admin_cert_names.all? { |cert| admin_cert_names.include?(cert) }
      
        # Check for the required coaching license
    #    has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '8U Coach').exists?
      
    #    has_required_admin_certs && has_required_license
    # end
end
