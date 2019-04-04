class AddArgListBinary < ActiveRecord::Migration[5.2]
  def change
    add_column("binary_debates", "for_arguments", :integer, array: true, default: [])
    add_column("binary_debates", "against_arguments", :integer, array: true, default: [])
  end
end
