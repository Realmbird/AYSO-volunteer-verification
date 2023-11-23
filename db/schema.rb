# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2023_11_23_100036) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "admin_details", force: :cascade do |t|
    t.string "cert_name"
    t.string "area"
    t.string "region"
    t.string "region_id"
    t.string "admin_id"
    t.string "admin_alt_id"
    t.datetime "reg_date"
    t.string "first_name"
    t.string "last_name"
    t.date "dob"
    t.string "gender"
    t.string "email"
    t.boolean "id_verified"
    t.string "id_verified_by"
    t.datetime "id_verified_date"
    t.datetime "risk_submit_date"
    t.string "risk_status"
    t.date "risk_expire_date"
    t.boolean "printed"
    t.datetime "photo_uploaded"
    t.string "coach_license_level"
    t.string "coach_license_num"
    t.date "coach_license_obtained_date"
    t.string "referee_grade"
    t.date "referee_grade_obtained_date"
    t.date "referee_expired_date"
    t.boolean "rostered"
    t.datetime "upload_date"
    t.boolean "verified"
    t.string "verified_by"
    t.datetime "verified_date"
    t.date "expired_date"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "license_details", force: :cascade do |t|
    t.string "section"
    t.string "area"
    t.string "region"
    t.integer "region_id"
    t.string "admin_id"
    t.integer "admin_alt_id"
    t.string "first_name"
    t.string "last_name"
    t.date "dob"
    t.string "gender"
    t.string "email"
    t.string "coaching_license_referee_grade"
    t.date "license_grade_obtained"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "players", force: :cascade do |t|
    t.string "program_name"
    t.string "division_name"
    t.string "account_first_name"
    t.string "account_last_name"
    t.string "player_first_name"
    t.string "player_last_name"
    t.string "player_gender"
    t.date "player_birth_date"
    t.string "street_address"
    t.string "unit"
    t.string "city"
    t.string "state"
    t.string "postal_code"
    t.string "user_email"
    t.string "telephone"
    t.string "cellphone"
    t.string "other_phone"
    t.string "team_name"
    t.datetime "order_date"
    t.integer "order_no"
    t.string "order_detail_description"
    t.decimal "orderitem_amount"
    t.decimal "orderitem_amount_paid"
    t.decimal "orderitem_balance"
    t.string "order_payment_status"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  create_table "volunteer_details", force: :cascade do |t|
    t.string "section"
    t.string "area"
    t.string "region"
    t.integer "region_id"
    t.string "admin_id"
    t.integer "admin_alt_id"
    t.string "first_name"
    t.string "last_name"
    t.date "dob"
    t.string "gender"
    t.string "email"
    t.string "coaching_license_referee_grade"
    t.date "license_grade_obtained"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "volunteers", force: :cascade do |t|
    t.string "program_name"
    t.string "division_name"
    t.string "team_name"
    t.string "volunteer_role"
    t.string "volunteer_first_name"
    t.string "volunteer_last_name"
    t.string "volunteer_street_address"
    t.string "volunteer_address_unit"
    t.string "volunteer_city"
    t.string "volunteer_state"
    t.string "volunteer_postal_code"
    t.string "volunteer_email_address"
    t.string "volunteer_telephone"
    t.string "volunteer_cellphone"
    t.string "volunteer_other_phone"
    t.integer "association_volunteer_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

end
