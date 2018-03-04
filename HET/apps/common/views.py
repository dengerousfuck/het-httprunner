from flask import Blueprint,request,make_response,jsonify
from exts import alidayu
from utils import restful,hetcache
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from io import BytesIO
import qiniu
from tasks import send_sms_captcha

bp = Blueprint('common',__name__,url_prefix='/c')


@bp.route('/')
def index():
    return 'common index'

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码')
#     captcha = Captcha.gene_text(number=4)
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         return restful.params_error(message='短信验证码发送失败！')

@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print('发送的短信验证码是：', captcha)
        # if alidayu.send_sms(telephone, code=captcha):
        #     hetcache.set(telephone,captcha)
        #     return restful.success()
        # else:
        #     return restful.params_error(message='短信验证码发送失败！')
        #     # hetcache.set(telephone, captcha)
        #     # return restful.success()
        send_sms_captcha(telephone,captcha)
        return restful.success()
    else:
        return restful.params_error(message='参数错误！')


@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text,image = Captcha.gene_graph_captcha()
    hetcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = 'tJLW2rNi_r60-2S_G2urRFzwg74lBarak-U4k9EE'#'M4zCEW4f9XPanbMN-Lb9O0S8j893f0e1ezAohFVL'
    secret_key = 'nVGDI0vihLlEbRQU6EoUz1thNi491aSH0_wS6iMa'#'7BKV7HeEKM3NDJk8_l_C89JI3SMmeUlAIatzl9d4'
    q = qiniu.Auth(access_key,secret_key)

    bucket = 'denger'#'hyvideo'
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})