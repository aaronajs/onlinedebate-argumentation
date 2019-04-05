class OpenDebate < ApplicationRecord

  has_many :arguments
  belongs_to :user

  scope :sorted, lambda { order("open_debates.updated_at DESC") }

  validates :description, :length => { :within => 1..280 }

end
