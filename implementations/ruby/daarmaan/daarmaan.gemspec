$:.push File.expand_path("../lib", __FILE__)

# Maintain your gem's version:
require "daarmaan/version"

# Describe your gem and declare its dependencies:
Gem::Specification.new do |s|
  s.name        = "Daarmaan"
  s.version     = Daarmaan::VERSION
  s.authors     = ["Sameer Rahmani"]
  s.email       = ["lxsameer@gnu.org"]
  s.homepage    = "http://daarmaan.yellowen.com"
  s.summary     = "Ruby implementation of Daarmaan client."
  s.description = "Ruby implementation of Daarmaan client."

  s.files = Dir["{app,config,db,lib}/**/*"] + ["LICENSE", "Rakefile", "README.rdoc"]
  s.test_files = Dir["test/**/*"]

  s.add_dependency "rails", "~> 3.2.8"
  s.add_dependency "ramp"
end
