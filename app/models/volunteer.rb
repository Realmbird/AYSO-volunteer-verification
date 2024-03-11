class Volunteer < ApplicationRecord
    # changes primary key
    self.primary_key = 'association_volunteer_id'
    
    #debug only
    def get_certs
        certfications = AdminDetail.where(admin_id: association_volunteer_id).select(:cert_name)
    end
    def get_special_cert
      certifications = AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Green').or(AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Blue')).where('expired_date > ? OR expired_date IS NULL', Date.today).where('risk_expire_date > ? OR risk_expire_date IS NULL', Date.today).select(:cert_name)
# For terminal
##AdminDetail.where(verified: true,risk_status: 'Green').where('risk_expire_date > ?', Date.today).select(:cert_name).distinct
## only safe sport has expired date
##AdminDetail.where(verified: true,risk_status: 'Green').where('risk_expire_date > ?', Date.today).where('expired_date > ?', Date.today).pluck(:cert_name).distinct
    end
    def get_coach_grades
        coach_grades = LicenseDetail.where(admin_id: association_volunteer_id).pluck(:coaching_license_referee_grade)
    end

    # volunteer requirements
    def universal_requirements
        required_admin_cert_names = ["AYSOs Safe Haven", "Concussion Awareness", "Sudden Cardiac Arrest"]
        admin_cert_names = AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Green').or(AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Blue')).where('expired_date > ? OR expired_date IS NULL', Date.today).where('risk_expire_date > ? OR risk_expire_date IS NULL', Date.today).pluck(:cert_name)
        has_required_admin_certs = required_admin_cert_names.all? { |cert| admin_cert_names.include?(cert) }
    end
    def advanced_requirements
        # Check green and blue
        # Check Safe Sport Expiration
        
        #Live Scan (state-required fingerprinting)
        #SafeSport (federally-mandated course) 
        required_admin_cert_names = ["SafeSport", "CA Mandated Fingerprinting"]
        admin_cert_names = AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Green').or(AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Blue')).where('expired_date > ? OR expired_date IS NULL', Date.today).where('risk_expire_date > ? OR risk_expire_date IS NULL', Date.today).pluck(:cert_name)
        has_required_admin_certs = required_admin_cert_names.all? { |cert| admin_cert_names.include?(cert) }
    end

    ##
    # First demo of compliance not used    
    #def is_8u_compliant?
     #   has_required_admin_certs = universal_coach_requirement
      
        # Check for the required coaching license
     #   has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '8U Coach').exists?
      
      #  has_required_admin_certs && has_required_license
    # end
    # coach levels

    #checked no expire date
    def is_6u_coach_compliant?
        has_required_admin_certs = universal_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '6U Coach').exists?
      
        has_required_admin_certs && has_required_license
     end
     #checked no expire date
     def is_8u_coach_compliant?
        has_required_admin_certs = universal_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '8U Coach').exists?
      
        has_required_admin_certs && has_required_license
     end

     #checked no expire date
     def is_10u_coach_compliant?
        has_required_admin_certs = universal_requirements
        #   has_required_federal_certs = advanced_requirements recommended
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '10U Coach').exists?
      
        has_required_admin_certs && has_required_license
     end

     #checked no expire date
     def is_12u_coach_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '12U Coach').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     #checked no expire date
     def is_14u_coach_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Intermediate (14U) Coach').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     #checked
     def is_19u_coach_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Advanced (19U) Coach').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end
    
     #checked
     def is_8u_ref_compliant?
        has_required_admin_certs = universal_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '8U Official').exists?
      
        has_required_admin_certs && has_required_license
     end

     #checked
     def is_10u_ref_compliant?
        has_required_admin_certs = universal_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Regional Referee').exists?
      
        has_required_admin_certs && has_required_license
     end

     #checked
     def is_12u_ref_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Intermediate Referee').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     #checked
     def is_14u_ref_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Advanced Referee').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     #checked
     def is_19u_ref_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'National Referee').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     def get_division_and_role(division_name)
         
     end

   # getting report 10u

     def self.all_compliant_10u_coaches
      Volunteer.all.select { |v| v.is_10u_coach_compliant? }
     end
     

end
