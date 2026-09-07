export default function handler(req, res) {
  res.setHeader('Set-Cookie',
    'sonar_session=; HttpOnly; Secure; Path=/; Max-Age=0; SameSite=Lax');
  res.status(200).send('Signed out of Sonar. Visit / to sign in again.');
}
