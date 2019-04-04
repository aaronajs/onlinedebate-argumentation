class Argument < ApplicationRecord

  acts_as_votable
  belongs_to :user

  scope :sorted, lambda { order("arguments.created_at DESC") }

  validates :description, :length => { :within => 1..280 }

  def create_json
    json = {
      "id" => self.id,
      "isLeading" => self.isLeading,
      "attacks" => self.attacks
    }
    return json
  end

end
