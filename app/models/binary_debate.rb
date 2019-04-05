class BinaryDebate < ApplicationRecord

  # binary debate belongs to only one user and has many arguments
  has_many :arguments
  belongs_to :user

  # sorted by most recently updated to oldest
  scope :sorted, lambda { order("binary_debates.updated_at DESC") }

  # description of max length 280 chars
  validates :description, :length => { :within => 1..280 }

end
