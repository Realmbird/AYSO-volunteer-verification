class ScrappersController < ApplicationController
    def setup
        download_directory = Rails.root.join('tmp', 'scraper_downloads')

        options = Selenium::WebDriver::Chrome::Options.new
        options.add_preference(:download, directory_upgrade: true, prompt_for_download: false, default_directory: download_directory.to_s)
        @driver = Selenium::WebDriver.for :chrome, options: options
    end 
    def sports_connect_login
        @driver.get('https://login.stacksports.com/login?client_id=612b0399b1854a002e427f78&redirect_uri=https://core-api.bluesombrero.com/login/redirect/portal/14685&app_name=Region+18&portalid=14685&instancekey=ayso')
        

        @driver.manage.timeouts.implicit_wait = 500

        #@driver.find_element(:link_text, 'Use another account?').click
        @driver.find_element(:name, 'email').click
        @driver.find_element(:name, 'email').send_keys(ENV["sports_username"])
        @driver.find_element(:name, 'continue').click
        element = @driver.find_element(:name, 'continue')
        @driver.find_element(:name, 'password').click
        @driver.find_element(:name, 'password').send_keys(ENV["sports_password"])
        @driver.find_element(:name, 'password').send_keys(:enter)
        @driver.find_element(:name, 'continue').click
        #@driver.find_element(:css, '.fa-bars').click
    end

    def sports_connect_enrollment_details
        #Webdrivers::Chromedriver.required_version = '91.0.4472.101'
        #setups webscrapper driver
        setup

        #logins to sports connect
        sports_connect_login

        click_with_retry(:id, 'BsbIconBar.ascx_ReportingSiteLinkMF')
        click_with_retry(:link_text, 'Most Visited')
        click_with_retry(:link_text, 'Volunteer Details')
        # clicks on save instead, this is the css selniuem gave me 
        #click_with_retry(:css, '.mat-menu-trigger .mat-icon')
        
        # Adding Index 
       
        begin
            wait = Selenium::WebDriver::Wait.new(timeout: 60)
            elements = wait.until {
                els = @driver.find_elements(:css, '.mat-focus-indicator.mat-button.mat-button-base.mat-primary')
                # Select only elements that are displayed and enabled
                els.size >= 4 ? els : nil
            }
            puts elements
            unique_element = elements[3]
            # Execute JavaScript to click the element
            @driver.execute_script("arguments[0].click();", unique_element)
        rescue Selenium::WebDriver::Error::StaleElementReferenceError, 
            Selenium::WebDriver::Error::NoSuchElementError, 
            Selenium::WebDriver::Error::ElementClickInterceptedError => e
            if (retries -= 1) > 0
                retry
            else
                raise e
            end
        end
        click_with_retry(:css, '.ng-star-inserted:nth-child(20) > .select')
        click_with_retry(:css, '.mat-flat-button')

        # Download with csv
        sleep(140)
        click_with_retry(:css, '.mat-focus-indicator.mat-menu-trigger.report-header-action.report-header-action__export.mat-button.mat-button-base.mat-primary.ng-star-inserted')
      
        click_with_retry(:css, '.mat-focus-indicator.mat-menu-item')
        sleep(60)
        @driver.quit

        csv_database_volunteer
    end
    def update
        csv_database_compliance
    end
    def csv_paser

    end
    def  csv_database_compliance
        csv_file_path1 = Rails.root.join('tmp', 'scraper_downloads', 'AdminLicenseGrade.csv')
        LicenseDetail.destroy_all
        license_parse_and_store_csv(csv_file_path1)

        if File.exist?(csv_file_path1)
            File.delete(csv_file_path1)
        end
        
        csv_file_path2 = Rails.root.join('tmp', 'scraper_downloads', 'AdminCredentialsStatusDynamic.csv')
        AdminDetail.destroy_all
        admin_parse_and_store_csv(csv_file_path2)
        # Check if the file exists before attempting to delete it
        if File.exist?(csv_file_path2)
            File.delete(csv_file_path2)
        end
        flash[:notice] =  'Compliance Data Successfully Scrapped.'
        redirect_to volunteers_path

    end
    
    def admin_parse_and_store_csv(csv_file_path)
        csv_mapping_admin = {
            #'Textbox333' => :section,
            'CertificateName' => :cert_name,
            'League' => :area,
            'Club' => :region,
            'ClubSID' => :region_id,
            'IDNUM1' => :admin_id,
            'AltID' => :admin_alt_id,
            'RegDate' => :reg_date,
            'FirstName' => :first_name,
            'LastName' => :last_name,
            'DOB' => :dob,
            'GenderCode' => :gender,
            'email' => :email,
            'IDVerified1' => :id_verified,
            'IDVerifiedBY1' => :id_verified_by,
            'IDVerifiedDate1' => :id_verified_date,
            'RiskSubmitDate' => :risk_submit_date,
            'RiskStatus' => :risk_status,
            'RiskExpireDate' => :risk_expire_date,
            'cardPrinted' => :printed,
            'photoInDate' => :photo_uploaded,
            'licLevel' => :coach_license_level,
            'licNum' => :coach_license_num,
            'LicObtainDate' => :coach_license_obtained_date,
            'refGrade1' => :referee_grade,
            'refObtainDate1' => :referee_grade_obtained_date,
            'refExpDate1' => :referee_expired_date,
            'rosteredYN' => :rostered,
            'ccInDate' => :upload_date,
            'ccVerified' => :verified,
            'ccVerifyBy' => :verified_by,
            'ccVerifyDate' => :verified_date,
            'ExpirationDateC' => :expired_date
            # Add other mappings as needed
        }
        CSV.foreach(csv_file_path, headers: true, header_converters: :symbol) do |row|
            volunteer_detail_attributes = csv_mapping_admin.each_with_object({}) do |(csv_header, model_attr), hash|
              hash[model_attr] = row[csv_header.downcase.to_sym] || row[csv_header]
            end
            AdminDetail.create(volunteer_detail_attributes)
        end
    end
    def license_parse_and_store_csv(csv_file_path)
        csv_mapping_lisence = {
            'Section' => :section,
            'Area' => :area,
            'Club_ID' => :region,
            'Admin_ID' => :region_id,
            'AdminID' => :admin_id,
            'AdminAltID' => :admin_alt_id,
            'First_Name' => :first_name,
            'Last_Name' => :last_name,
            'DOB' => :dob,
            'Gender' => :gender,
            'Email' => :email,
            'LicenseLevel' => :coaching_license_referee_grade,
            'Risk_Submit_Date' => :license_grade_obtained,
        }
       
        CSV.foreach(csv_file_path, headers: true, header_converters: :symbol) do |row|
            volunteer_detail_attributes = csv_mapping_lisence.each_with_object({}) do |(csv_header, model_attr), hash|
              hash[model_attr] = row[csv_header.downcase.to_sym] || row[csv_header]
            end
            LicenseDetail.create(volunteer_detail_attributes)
        end
    end
    
  
    

    def volunteer1_parse_and_store_csv(csv_file_path)
        CSV.foreach(csv_file_path, headers: true, header_converters: :symbol) do |row|
          Volunteer.create(row.to_hash)
        end
    end
     
    def csv_database_volunteer
        csv_file_path = Rails.root.join('tmp', 'scraper_downloads', 'Volunteer_Details.csv')
        Volunteer.destroy_all
        volunteer1_parse_and_store_csv(csv_file_path)
        
        # Check if the file exists before attempting to delete it
        if File.exist?(csv_file_path)
            File.delete(csv_file_path)
        end
        flash[:notice] =  'Volunteer Data Successfully Scrapped.'
        redirect_to volunteers_path
    end

    def click_with_retry(by, selector, retries=3)
        begin
            wait = Selenium::WebDriver::Wait.new(timeout: 60)
            element = wait.until {
                el = @driver.find_element(by, selector)
                el if el.displayed? && el.enabled?
            }
            # Execute JavaScript to click the element
            @driver.execute_script("arguments[0].click();", element)
        rescue Selenium::WebDriver::Error::StaleElementReferenceError, 
            Selenium::WebDriver::Error::NoSuchElementError, 
            Selenium::WebDriver::Error::ElementClickInterceptedError => e
            if (retries -= 1) > 0
                retry
            else
                raise e
            end
        end
    end

    def compliance_login
        @driver.get('https://eayso.sportsaffinity.com/Foundation/Login.aspx?sessionguid=')
        @driver.manage.timeouts.implicit_wait = 500
        @driver.find_element(:id, 'loginControl_btnSSOLogin').click
        @driver.find_element(:name, 'email').click
        @driver.find_element(:name, 'email').send_keys(ENV["sports_username"])
        @driver.find_element(:name, 'continue').click
        @driver.find_element(:name, 'password').click
        @driver.find_element(:name, 'password').send_keys(ENV["sports_password"])
        @driver.find_element(:name, 'password').send_keys(:enter)
    end
    def compliance_details
        #setups webscrapper driver
        setup

        #logins to sports affinity
        compliance_login

        # goes to additional reports page
        compliance_additional_reports

        compliance_download
    
        csv_database_compliance
        
    end

    def compliance_additional_reports
        # Wait for the page to load and for the URL to contain 'sessionguid'
        wait = Selenium::WebDriver::Wait.new(timeout: 10)
        wait.until { @driver.current_url.include?('sessionguid') }

        # Parse the current URL to extract the 'sessionguid'
        current_url = @driver.current_url
        uri = URI.parse(current_url)
        params = URI.decode_www_form(uri.query).to_h
        sessionguid = params['sessionguid']
         # Construct the URL for 'Additional Reports'

        additional_reports_url = "https://eayso.sportsaffinity.com/reg/reportsstats/newreports.asp?sessionguid=#{sessionguid}&type=B"

        # Navigate to the 'Additional Reports' page
        @driver.get additional_reports_url
    end
    def compliance_download
        compliance_download_admin
        sleep(10)
        compliance_download_credentials
    end

    def compliance_download_admin
        @driver.find_element(:id, 'reporttype').click
        @driver.find_element(:css, 'option[value="143"]').click()
        
        # Selects Region 18
        @driver.find_element(:id, 'Select6').click
        select_element = @driver.find_element(name: 'club')
        select = Selenium::WebDriver::Support::Select.new(select_element)
        select.select_by(:text, 'Region 18')
       
        #original window
        original_window = @driver.window_handle

        # Enters seperate screen
        @driver.find_element(:id, 'Button2').click
        
        # switches to new window code not sure how to do
       
        # Wait for the new window or tab to appear and switch to it
        @wait = Selenium::WebDriver::Wait.new(timeout: 10)
        @wait.until { @driver.window_handles.size > 1 }
        new_window_handle = (@driver.window_handles - [original_window]).first
        @driver.switch_to.window(new_window_handle)
        select_element = @driver.find_element(name: 'ctrlRptViewer$ctl01$ctl05$ctl00')
        select = Selenium::WebDriver::Support::Select.new(select_element)
        select.select_by(:text, 'CSV (comma delimited)')
     
        @driver.find_element(:id, 'ctrlRptViewer_ctl01_ctl05_ctl01').click
        
        @driver.close
        @driver.switch_to.window(original_window)


        #dropdown = @driver.find_element(:id, 'Select6')
        #dropdown.find_element(:xpath, "//option[. = 'Region 18']").click
        #@driver.find_element(:css, '#Select6 > option:nth-child(2)').click
    end
    def compliance_download_credentials
        @driver.find_element(:id, 'reporttype').click
        @driver.find_element(:css, 'option[value="148"]').click()

        #original Window
        original_window = @driver.window_handle

        #opens new window
        @driver.find_element(:id, 'Button2').click

        @wait = Selenium::WebDriver::Wait.new(timeout: 10)
        @wait.until { @driver.window_handles.size > 1 }
        new_window_handle = (@driver.window_handles - [original_window]).first
        @driver.switch_to.window(new_window_handle)
        select_element = @driver.find_element(name: 'ctrlRptViewer$ctl01$ctl05$ctl00')
        select = Selenium::WebDriver::Support::Select.new(select_element)
        select.select_by(:text, 'CSV (comma delimited)')
        @driver.find_element(:id, 'ctrlRptViewer_ctl01_ctl05_ctl01').click()
        @driver.close
        @driver.switch_to.window(original_window)
        @driver.close
        
    end

    def universal_scrape
        sports_connect_enrollment_details
        compliance_details
    end

end