class ScrappersController < ApplicationController
    def setup
        download_directory = Rails.root.join('tmp', 'scraper_downloads')

        options = Selenium::WebDriver::Chrome::Options.new
        options.add_preference(:download, directory_upgrade: true, prompt_for_download: false, default_directory: download_directory.to_s)
        @driver = Selenium::WebDriver.for :chrome, options: options
    end 
    def sports_login
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
        sports_login

        click_with_retry(:id, 'BsbIconBar.ascx_ReportingSiteLinkMF')
        click_with_retry(:link_text, 'Most Visited')
        click_with_retry(:link_text, 'Enrollment Details')
        # clicks on save instead, this is the css selniuem gave me 
        #click_with_retry(:css, '.mat-menu-trigger .mat-icon')
        click_with_retry(:css, '.mat-focus-indicator.mat-menu-trigger.report-header-action.report-header-action__export.mat-button.mat-button-base.mat-primary.ng-star-inserted')
        
        click_with_retry(:css, '.mat-focus-indicator.mat-menu-item')
        sleep(10)
        @driver.quit

        parse_and_store_csv("tmp/scraper_downloads/Enrollment_Details.csv")
        File.delete("tmp/scraper_downloads/Enrollment_Details.csv") if File.exist?("/tmp/scraper_downloads/Enrollment_Details.csv")

        flash[:notice] =  'Selenium test executed successfully.'
        redirect_to users_path
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

    def parse_and_store_csv(csv_file_path)
        CSV.foreach(csv_file_path, headers: true, header_converters: :symbol) do |row|
          Player.create(row.to_hash)
        end
    end

end