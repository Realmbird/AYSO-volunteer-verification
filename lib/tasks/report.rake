#auto imports compliance coaches

desc "Makes Volunteer Compliance data"
task report: :environment do
  compliant_volunteers_by_division_and_role = Volunteer.all_compliant

  compliant_volunteers_by_division_and_role.each do |division_role, volunteers|
    compliant_volunteers_json = volunteers.as_json
    file_name = "compliant_#{division_role.downcase.gsub('/', '_').gsub(' ', '_')}.json"

    File.open(file_name, 'w') do |file|
      file.write(compliant_volunteers_json.to_json)
    end
  end
end