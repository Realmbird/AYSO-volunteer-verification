#auto imports compliance coaches

desc "Makes Volunteer Compliance data"
task report: :environment do
    # This could be run in a rails console or a rake task
    compliant_coaches = Volunteer.all_compliant_10u_coaches
    compliant_coaches_json = compliant_coaches.as_json

    File.open('compliant_10u_coaches.json', 'w') do |file|
        file.write(compliant_coaches_json.to_json)
    end

end