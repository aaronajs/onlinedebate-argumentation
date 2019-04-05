class Argument < ApplicationRecord

  # is voted on by different users
  # belongs to only one user
  acts_as_votable
  belongs_to :user

  # sorted by most recently created
  scope :sorted, lambda { order("arguments.created_at DESC") }

  # description max length 280 chars
  validates :description, :length => { :within => 1..280 }

  # creates json object of Argument
  # only contains the id, is leading boolean, and list of attacks
  def create_json
    json = {
      "id" => self.id,
      "isLeading" => self.isLeading,
      "attacks" => self.attacks
    }
    return json
  end

end
