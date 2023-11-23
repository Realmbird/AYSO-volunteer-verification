class CreateLicenseDetails < ActiveRecord::Migration[7.0]
  def change
    create_table :license_details do |t|
      t.string :section
      t.string :area
      t.string :region
      t.integer :region_id
      t.string :admin_id
      t.integer :admin_alt_id
      t.string :first_name
      t.string :last_name
      t.date :dob
      t.string :gender
      t.string :email
      t.string :coaching_license_referee_grade
      t.date :license_grade_obtained

      t.timestamps
    end
  end
end
