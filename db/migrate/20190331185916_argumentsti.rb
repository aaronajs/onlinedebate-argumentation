class Argumentsti < ActiveRecord::Migration[5.2]
  # def up
  #   drop_table :arguments
  #   create_table :arguments do |t|
  #     t.string :type
  #     t.string "description", limit: 280, null: false
  #     t.integer "attacks", array: true, default: []
  #     t.integer "defends", array: true, default: []
  #     t.integer "user_id", null: false
  #     t.integer "debate_id", null: false
  #     t.integer "rating", default: 0, null: false
  #     t.integer "reported", default: 0, null: false
  #     t.timestamps
  #   end
  # end
  #
  # def down
  #   drop_table :arguments
  #   create_table :arguments do |t|
  #     t.string "description", limit: 280, null: false
  #     t.integer "attacks", array: true, default: []
  #     t.integer "defends", array: true, default: []
  #     t.integer "user_id", null: false
  #     t.integer "debate_id", null: false
  #     t.integer "rating", default: 0, null: false
  #     t.integer "reported", default: 0, null: false
  #     t.timestamps
  #   end
  #   add_column("arguments", "isOpen", :boolean, null: false)
  # end
  def change
  end
end
