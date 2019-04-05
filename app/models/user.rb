class User < ApplicationRecord

  # sets user to have an assigned vote for each argument
  acts_as_voter
  # sets user to have a hashed password
  has_secure_password

  # a user can have many arguments and debates
  has_many :open_debates
  has_many :binary_debates
  has_many :arguments

  # when called, lists the users in a list in descending order by age
  scope :sorted, lambda { order("users.created_at DESC") }

  # regexes to compare email addresses and passwords to
  # they must match the regex or they won't be accepted
  EMAIL_REGEX = /\A[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}\Z/i
  PASSWORD_REGEX = /(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{5,}/

  # username must be unique and be between 1-25 characters
  # email must be present, unique, max 100 chars and match the EMAIL_REGEX
  # passwords must be present and match PASSWORD_REGEX
  validates :username, :length => { :within => 1..25 },
                       :uniqueness => true
  validates :email, :presence => true,
                    :uniqueness => true,
                    :length => { :maximum => 100 },
                    :format => EMAIL_REGEX,
                    :confirmation => true
  validates :password_digest, :presence => true,
                         :format => PASSWORD_REGEX;

end
