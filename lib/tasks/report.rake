#auto imports compliance coaches

desc "Makes Volunteer Compliance data"
task report: :environment do
  # Define the target folder name
  folder_name = "compliance_reports"
  directory_path = Rails.root.join(folder_name)
  # Create the directory unless it already exists
  Dir.mkdir(directory_path) unless Dir.exist?(directory_path)

  compliant_volunteers_by_division_and_role = Volunteer.all_compliant

  compliant_volunteers_by_division_and_role.each do |division_role, volunteers|
    compliant_volunteers_json = volunteers.as_json
    file_name = "compliant_#{division_role.downcase.gsub('/', '_').gsub(' ', '_')}.json"

    # Specify the path where the file will be saved
    file_path = File.join(directory_path, file_name)
    File.open(file_path, 'w') do |file|
      file.write(compliant_volunteers_json.to_json)
    end
  end
end