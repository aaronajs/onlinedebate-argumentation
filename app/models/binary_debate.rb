class BinaryDebate < ApplicationRecord

  has_many :arguments
  belongs_to :user
  
  scope :sorted, lambda { order("binary_debates.updated_at DESC") }

  validates :description, :length => { :within => 1..280 },
                          :uniqueness => true

end
