class AddDefaultLeader < ActiveRecord::Migration[5.2]
  def change
    change_column("open_debates", "leader", :integer, default: 0)
  end
end
