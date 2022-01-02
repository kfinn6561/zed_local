function get_from_metadata {
  curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/attributes/${1}"
}

chrome_tools_folder="${HOME}/chrome_tools"
export CHROMEDRIVER_PATH="${chrome_tools_folder}/chromedriver"

# Metadata should be set in the "bucket-name" attribute using the "gs://mybucketname/" format.
worker_bucket=$(get_from_metadata "bucket-name")
export BUCKET_NAME=$worker_bucket

# Metadata should be set in the "bucket-name" attribute using the "gs://mybucketname/" format.
bids_filename=$(get_from_metadata "bids-filename")
export BIDS_URL="${worker_bucket}/${bids_filename}"

#copy metamask extension files
extension_name="10.7.1_0"
export METAMASK_EXTENSION_PATH="${chrome_tools_folder}/${extension_name}"

#get metamask secret phrase from gcp secret manager
metamask_secret_id=$(get_from_metadata "metamask-secret-id")
export METAMASK_PHRASE=$(gcloud secrets versions access latest --secret="${metamask_secret_id}")
metamask_password_id=$(get_from_metadata "metamask-password-secret")
export METAMASK_PASSWORD=$(gcloud secrets versions access latest --secret="${metamask_password_id}")

#get proxy username and password from gcp secret manager
proxy_username_secret_id=$(get_from_metadata "proxy-username-secret-id")
export PROXY_USERNAME=$(gcloud secrets versions access latest --secret="${proxy_username_secret_id}")
proxy_password_secret_id=$(get_from_metadata "proxy-password-secret-id")
export PROXY_PASSWORD=$(gcloud secrets versions access latest --secret="${proxy_password_secret_id}")

#clone source code
git_source=$(get_from_metadata "git-source")