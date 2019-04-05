require 'test_helper'

class AccessControllerTest < ActionDispatch::IntegrationTest

  setup do
    @user = build(:user)
  end

  test "should get login" do
    get :login
    assert_response :success
  end

  test "should get signup" do
    get :signup
    assert_response :success
  end

end
