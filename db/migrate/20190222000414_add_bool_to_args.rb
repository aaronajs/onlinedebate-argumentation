class AddBoolToArgs < ActiveRecord::Migration[5.2]
  def change
    add_column("arguments", "isOpen", :boolean, null: false)
  end
end
