class AddBanDate < ActiveRecord::Migration[5.2]
  def change
    add_column("users", "ban_date", :datetime)
  end
end
