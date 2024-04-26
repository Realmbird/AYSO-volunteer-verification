require 'caxlsx'
namespace :volunteer_data do
    desc "Generate JSON files for volunteer data by division"
    task :to_json => :environment do
        # Define the target folder name
        folder_name = "volunteer_reports"
        directory_path = Rails.root.join(folder_name)
        # Create the directory unless it already exists
        Dir.mkdir(directory_path) unless Dir.exist?(directory_path)

        Volunteer.divisional_data.each do |division_code, data|
            # Define the file name
            file_name = "#{division_code}_compliance.json"

            # Specify the path where the file will be saved
            file_path = File.join(directory_path, file_name)

            # Write data to the file
            File.open(file_path, "w") do |file|
                file.write(data.to_json)
            end
        end
    end
  
  desc "Generate Excel files for volunteer data by division"
  task :to_excel => :environment do
    folder_name = "volunteer_reports"
    directory_path = Rails.root.join(folder_name)
  
    # Create the directory unless it already exists
    Dir.mkdir(directory_path) unless Dir.exist?(directory_path)
  
    Axlsx::Package.new do |package|
      Volunteer.divisional_data.each do |division_code, volunteers|
        # For each division, create a new worksheet
        package.workbook.add_worksheet(name: division_code) do |sheet|
          # Here you would add your headers
          sheet.add_row ['First', 'Last', 'Email', 'Role', 'Division', 'Safe Haven', 'Concussion', 'Cardiac', 'SafeSport', 'Live Scan', 'Compliant']
  
          # Then add each volunteer's data as a new row
          volunteers.each do |volunteer|
            sheet.add_row [
              volunteer[:first_name],
              volunteer[:last_name],
              volunteer[:email],
              volunteer[:role],
              volunteer[:division],
              volunteer[:safe_haven],
              volunteer[:concussion],
              volunteer[:cardiac],
              volunteer[:safesport],
              volunteer[:live_scan],
              volunteer[:compliant] ? 'Yes' : 'No'
            ]
          end
        end
      end
  
      # Serialize the Excel file to disk
      package.serialize(File.join(directory_path, 'volunteer_data.xlsx'))
    end
  end
  end