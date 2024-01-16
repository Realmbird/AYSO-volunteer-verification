class AddForeignKeyToAdminDetails < ActiveRecord::Migration[7.0]
  def change
    add_foreign_key :admin_details, :volunteers, column: :admin_id, primary_key: :association_volunteer_id
  end
end
