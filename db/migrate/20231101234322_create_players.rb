class CreatePlayers < ActiveRecord::Migration[7.0]
  def change
    create_table :players do |t|
      t.string :program_name
      t.string :division_name
      t.string :account_first_name
      t.string :account_last_name
      t.string :player_first_name
      t.string :player_last_name
      t.string :player_gender
      t.date :player_birth_date
      t.string :street_address
      t.string :unit
      t.string :city
      t.string :state
      t.string :postal_code
      t.string :user_email
      t.string :telephone
      t.string :cellphone
      t.string :other_phone
      t.string :team_name
      t.datetime :order_date
      t.integer :order_no
      t.string :order_detail_description
      t.decimal :orderitem_amount
      t.decimal :orderitem_amount_paid
      t.decimal :orderitem_balance
      t.string :order_payment_status

      t.timestamps
    end
  end
end
