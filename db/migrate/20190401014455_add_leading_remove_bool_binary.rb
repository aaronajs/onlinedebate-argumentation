class AddLeadingRemoveBoolBinary < ActiveRecord::Migration[5.2]
  def change
    add_column("arguments", "isLeading", :boolean, default: false, null: false)
  end
end
