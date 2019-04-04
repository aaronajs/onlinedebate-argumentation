class User < ApplicationRecord

  acts_as_voter
  has_secure_password

  has_many :open_debates
  has_many :binary_debates
  has_many :arguments

  scope :sorted, lambda { order("users.created_at DESC") }

  EMAIL_REGEX = /\A[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}\Z/i
  PASSWORD_REGEX = /(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{5,}/

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
