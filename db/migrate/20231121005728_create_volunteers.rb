class CreateVolunteers < ActiveRecord::Migration[7.0]
  def change
    create_table :volunteers do |t|
      t.string :program_name
      t.string :division_name
      t.string :team_name
      t.string :volunteer_role
      t.string :volunteer_first_name
      t.string :volunteer_last_name
      t.string :volunteer_street_address
      t.string :volunteer_address_unit
      t.string :volunteer_city
      t.string :volunteer_state
      t.string :volunteer_postal_code
      t.string :volunteer_email_address
      t.string :volunteer_telephone
      t.string :volunteer_cellphone
      t.string :volunteer_other_phone
      t.integer :association_volunteer_id

      t.timestamps
    end
  end
end
