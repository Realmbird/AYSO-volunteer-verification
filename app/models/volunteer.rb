class Volunteer < ApplicationRecord
    # changes primary key
   #  self.primary_key = 'association_volunteer_id'
    

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
      has_required_federal_certs = advanced_requirements
    
      # Check for the required coaching license
      has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '10U Coach').exists?
    
      has_required_admin_certs && has_required_license && has_required_federal_certs
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
     def is_8u_referee_compliant?
        has_required_admin_certs = universal_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: '8U Official').exists?
      
        has_required_admin_certs && has_required_license
     end

     #checked
     def is_10u_referee_compliant?
        has_required_admin_certs = universal_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Regional Referee').exists?
      
        has_required_admin_certs && has_required_license
     end

     #checked
     def is_12u_referee_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Intermediate Referee').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     #checked
     def is_14u_referee_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'Advanced Referee').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     #checked
     def is_19u_referee_compliant?
        has_required_admin_certs = universal_requirements
        has_required_federal_certs = advanced_requirements
      
        # Check for the required coaching license
        has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'National Referee').exists?
      
        has_required_admin_certs && has_required_license && has_required_federal_certs
     end

     def get_division()
      # Extracts the numeric age part (assumes 1 or 2 digits) followed by 'U' and then the gender character ('B' or 'G')
      if match = division_name.match(/(\d{1,2})U(B|G)/)
        division_age = match[1]  # The numeric part, e.g., '8' or '10'
        gender = match[2]  # 'B' or 'G'

        # Construct the division code UB or UG
        division_code = "#{division_age}U#{gender}"

        division_num = "#{division_age}"
    
        # Return the extracted division code
        return division_num 
      else
        # Handle case where division_name does not match expected pattern
        return nil
      end
    end
    def get_division_code
      match = division_name.match(/(\d{1,2})U(B|G)/)
      match ? "#{match[1]}U#{match[2]}" : nil
    end
    def self.convert_division_code(division_code) # converts division_code to number
      match = division_code.match(/(\d{1,2})U(B|G)/)
      match ? match[1] : nil  # Just return the numeric part
    end
    def self.nearest_compliance_division(division_num)
      # Return nil if division_num is nil
      return nil if division_num.nil?
    
      # Convert division_num to an integer for comparison
      rounded_division = division_num.to_i
      
      # If division is 19, return it as is
      return '19' if rounded_division == 19
      
      # Round up to the next even number for coach compliance, unless it's already even
      rounded_division += 1 if rounded_division.odd? && rounded_division != 19
      
      # Return the adjusted division number as a string
      rounded_division.to_s
    end
    
    

    def get_role()
      # Cleans roles into Coach and Referee
      return 'Coach' if volunteer_role&.include?('Coach')
      return 'Referee' if volunteer_role&.include?('Referee')
      nil
   end
   def get_roles # updated
      roles = []
      roles << 'Coach' if volunteer_role&.include?('Coach')
      roles << 'Referee' if volunteer_role&.include?('Referee')
      roles
   end
    


   def get_missing_certs
      division_num = get_division.to_i
      role = get_role
      # Define basic and advanced certifications
      basic_admin_cert_names = ["AYSOs Safe Haven", "Concussion Awareness", "Sudden Cardiac Arrest"]
      advanced_admin_cert_names = ["SafeSport", "CA Mandated Fingerprinting"]
    
      # Determine required certifications based on role and division
      required_certs = basic_admin_cert_names
      if role == "Coach" && division_num >= 10 || role == "Referee" && division_num >= 12
        required_certs += advanced_admin_cert_names
      end
    
      # Fetch the volunteer's existing certifications
      existing_cert_names = AdminDetail.where(admin_id: association_volunteer_id).pluck(:cert_name).uniq
    
      # Identify missing certifications
      missing_certs = required_certs - existing_cert_names
    
      # Return the list of missing certifications
      missing_certs
    end
    
   def is_compliant
      division_num = get_division #gets first division
      role = get_role #gets first role

      return false if division_num.nil? || role.nil?

      compliance_method = "is_#{division_num}u_#{role.downcase}_compliant?".to_sym
      if self.respond_to?(compliance_method)
         self.send(compliance_method) # actually call the method if it exists
      else
         false
      end
   end
   def is_compliant_specific(role, division)
      # has_required_license = LicenseDetail.where(admin_id: association_volunteer_id, coaching_license_referee_grade: 'National Referee').exists?
      division_num = division
      division_num = Volunteer.nearest_compliance_division(division_num)
      role = role.to_s.downcase

      return false if division_num.nil? || role.nil?

      compliance_method = "is_#{division_num}u_#{role.downcase}_compliant?".to_sym
      if self.respond_to?(compliance_method)
         self.send(compliance_method) # actually call the method if it exists
      else
         false
      end
   end

   #formatting for form
   def get_cert_status_exclude_null(cert_name)
      # where(admin_id: association_volunteer_id, verified: true, risk_status: 'Green').or(AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Blue')).where('expired_date > ? OR expired_date IS NULL', Date.today).where('risk_expire_date > ? OR risk_expire_date IS NULL', Date.today).pluck(:cert_name)

      #  Checks if admin detail exists for certname and if not expired
      AdminDetail.where(admin_id: association_volunteer_id, cert_name: cert_name, risk_status: 'Green').or(AdminDetail.where(admin_id: association_volunteer_id, verified: true,cert_name: cert_name, risk_status: 'Blue'))
      .where('expired_date > ?', Date.today)
      .where('risk_expire_date > ?', Date.today)
      .exists? ? 'x' : '-'
    end
    def get_cert_status(cert_name)
      # where(admin_id: association_volunteer_id, verified: true, risk_status: 'Green').or(AdminDetail.where(admin_id: association_volunteer_id, verified: true, risk_status: 'Blue')).where('expired_date > ? OR expired_date IS NULL', Date.today).where('risk_expire_date > ? OR risk_expire_date IS NULL', Date.today).pluck(:cert_name)

      #  Checks if admin detail exists for certname and if not expired
      AdminDetail.where(admin_id: association_volunteer_id, cert_name: cert_name)
      .where('expired_date > ? OR expired_date IS NULL', Date.today)
      .where('risk_expire_date > ? OR risk_expire_date IS NULL', Date.today)
      .exists? ? 'x' : '-'
    end

   def formatted_data(division_num, role, division_code)
      # add vol status and coaching_license_referee_grade from license detail
      {
        first_name: volunteer_first_name,
        last_name: volunteer_last_name,
        email: volunteer_email_address,
        division: division_code,
        safe_haven: get_cert_status("AYSOs Safe Haven"),
        concussion: get_cert_status("Concussion Awareness"),
        cardiac: get_cert_status("Sudden Cardiac Arrest"),
        safesport: get_cert_status("SafeSport"),
        live_scan: get_cert_status("CA Mandated Fingerprinting"),
        compliant: is_compliant_specific(role, division_num),
        role: role
      }
   end    
    # This method gathers all volunteers' formatted data organized by division code
  def self.divisional_data
   # Initialize a hash to store the volunteers' data by division code
   divisional_data = {}

   # Iterate over all volunteers
   all.find_each do |volunteer|
    volunteer.get_roles.each do |role|
      division_num = convert_division_code(volunteer.get_division_code)
      division_code = volunteer.get_division_code
      next if division_num.nil?

      divisional_data[division_code] ||= []

      divisional_data[division_code] << volunteer.formatted_data(division_num, role, division_code)
      end
   end

      divisional_data
   end
      
      
   def self.all_compliant
      compliant_volunteers = {}
    
      Volunteer.all.each do |volunteer|
        division_num = volunteer.get_division
        role = volunteer.get_role
        next unless division_num && role  # Skip if division or role cannot be determined
    
        compliance_method = "is_#{division_num}u_#{role.downcase}_compliant?".to_sym
        if volunteer.respond_to?(compliance_method) && volunteer.send(compliance_method)
          division_role_key = "#{division_num}U#{role}"
          compliant_volunteers[division_role_key] ||= []
          compliant_volunteers[division_role_key] << volunteer
        end
      end
    
      compliant_volunteers
    end
    
    
   # getting report 10u

     def self.all_compliant_10u_coaches
      Volunteer.all.select { |v| v.is_10u_coach_compliant? }
     end
     

end
