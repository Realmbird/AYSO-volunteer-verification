class CreateAdminDetails < ActiveRecord::Migration[7.0]
  def change
    create_table :admin_details do |t|
      t.string :cert_name
      t.string :area
      t.string :region
      t.string :region_id
      t.string :admin_id
      t.string :admin_alt_id
      t.datetime :reg_date
      t.string :first_name
      t.string :last_name
      t.date :dob
      t.string :gender
      t.string :email
      t.boolean :id_verified
      t.string :id_verified_by
      t.datetime :id_verified_date
      t.datetime :risk_submit_date
      t.string :risk_status
      t.date :risk_expire_date
      t.boolean :printed
      t.datetime :photo_uploaded
      t.string :coach_license_level
      t.string :coach_license_num
      t.date :coach_license_obtained_date
      t.string :referee_grade
      t.date :referee_grade_obtained_date
      t.date :referee_expired_date
      t.boolean :rostered
      t.datetime :upload_date
      t.boolean :verified
      t.string :verified_by
      t.datetime :verified_date
      t.date :expired_date

      t.timestamps
    end
  end
end
