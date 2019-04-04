class AddDebatesAndArguments < ActiveRecord::Migration[5.2]
  def up
    create_table :open_debates do |t|
      t.string "description", limit: 280, null: false
      t.integer "leader"
      t.integer "user_id", null: false
      t.integer "reported", default: 0, null: false
      t.timestamps
    end

    create_table :binary_debates do |t|
      t.string "description", limit: 280, null: false
      t.string "for", limit: 100, null: false
      t.string "against", limit: 100, null: false
      t.boolean "isFor", default: true
      t.integer "user_id", null: false
      t.integer "reported", default: 0, null: false
      t.timestamps
    end

    create_table :arguments do |t|
      t.string "description", limit: 280, null: false
      t.integer "attacks", array: true, default: []
      t.integer "defends", array: true, default: []
      t.integer "user_id", null: false
      t.integer "debate_id", null: false
      t.integer "rating", default: 0, null: false
      t.integer "reported", default: 0, null: false
      t.timestamps
    end
  end

  def down
    drop_table :arguments
    drop_table :binary_debates
    drop_table :open_debates
  end
end
