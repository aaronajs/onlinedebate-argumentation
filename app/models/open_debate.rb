class OpenDebate < ApplicationRecord

  # open debates belong to one user only and have many arguments
  has_many :arguments
  belongs_to :user

  # sorted by most recently updated to oldest
  scope :sorted, lambda { order("open_debates.updated_at DESC") }

  # must have a description of max 280 characters
  validates :description, :length => { :within => 1..280 }

end
