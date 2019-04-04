class RemoveRatings < ActiveRecord::Migration[5.2]
  def change
    remove_column("arguments", "rating")
  end
end
