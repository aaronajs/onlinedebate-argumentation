class AddUsers < ActiveRecord::Migration[5.2]
  def up
    create_table :users do |t|
      t.string "username", limit: 25, null: false
      t.string "email", limit: 100, null: false
      t.integer "reported", default: 0, null: false
      t.string "password_digest", null: false
      t.timestamps
    end
  end

  def down
    drop_table :users
  end
end
