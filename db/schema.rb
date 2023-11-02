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

ActiveRecord::Schema[7.0].define(version: 2023_11_01_234322) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

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

  create_table "vehicles", force: :cascade do |t|
    t.string "title"
    t.string "stock_type"
    t.string "exterior_color"
    t.string "interior_color"
    t.string "transmission"
    t.string "drivetrain"
    t.integer "price"
    t.integer "miles"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "vehicles_spiders", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "volunteers", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

end
