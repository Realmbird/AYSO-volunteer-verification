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
  
    # Similar task for generating an Excel file
    # ...
  end